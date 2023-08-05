from datetime import datetime, timedelta

import click
import cloup
import InquirerPy.inquirer as inquirer
from bpkio_api.helpers.handlers import ContentHandler, factory
from bpkio_api.helpers.source_type import SourceTypeDetector
from bpkio_api.helpers.times import relative_time
from bpkio_api.models import (
    AssetSourceIn,
    LiveSourceIn,
    SourceType,
    VirtualChannelService,
    VirtualChannelSlotIn,
    VirtualChannelSlotType,
)

import bpkio_cli.utils.inquirer as inqdef
from bpkio_cli.core.app_context import AppContext
from bpkio_cli.core.config_provider import ConfigProvider
from bpkio_cli.utils.datetimes import (
    parse_date_expression_as_utc,
    parse_duration_expression,
)


def populate_virtual_channel_slots_command():
    # COMMAND: POPULATE
    @cloup.command(help="Populate the slots of a Virtual Channel service")
    @click.pass_obj
    def populate(obj: AppContext):
        api = obj.api.services.virtual_channel
        vc_id = obj.resources.last()
        vc: VirtualChannelService = api.retrieve(vc_id)

        all_sources = obj.api.sources.list()

        # Define source list
        slot_sources = [
            s
            for s in all_sources
            if s.type in (SourceType.LIVE, SourceType.ASSET) and s.format == vc.format
        ]
        slot_sources = sorted(slot_sources, key=lambda s: s.id, reverse=True)
        slot_sources = obj.cache.sort_resources_by_most_recently_accessed(slot_sources)
        choices = [
            dict(value=s.id, name=f"({s.id})  {s.name}  [{s.type.value}]")
            for s in slot_sources
        ]

        choices = [dict(value="BYURL", name="-- From URL --")] + choices

        if vc.adBreakInsertion is not None:
            choices = [dict(value="ADBREAK", name="-- Ad Break --")] + choices

        choices = [dict(value=None, name="-- End of schedule --")] + choices

        # Ask for a starting time
        starting_in = inquirer.text(
            message="Starting time",
            default="now",
            **inqdef.markers(),
            filter=lambda t: parse_date_expression_as_utc(t),
            transformer=lambda t: relative_time(parse_date_expression_as_utc(t)),
            long_instruction="Use an exact time, or a time expression "
            "(eg. 'in 10 min', 'tomorrow 10am', 'now')",
        ).execute()

        # Check if there are slots starting at that time (and in the next 4 hours)
        existing_slots = api.slots.list(
            vc.id, from_time=starting_in, to_time=starting_in + timedelta(hours=4)
        )
        if existing_slots:
            clear = inquirer.confirm(
                message="There are already slots in this channel for that starting time. "
                "Would you like to clear all future slots?",
                default=False,
                **inqdef.markers(),
            ).execute()

            if clear:
                (deleted, failed) = api.slots.clear(vc_id)
            else:
                raise click.Abort

        schedule = []
        t0 = datetime.utcnow().replace(microsecond=0) + timedelta(seconds=20)

        click.secho("\nDefine schedule for the channel", fg="yellow")
        adbreak_default_duration = "2 min"
        while True:
            # Ask for a source
            msg = "Source to add" if len(schedule) == 0 else "Next source to add"
            source_id = inquirer.fuzzy(
                message=msg, choices=choices, **inqdef.select_markers(0)
            ).execute()

            # Stop the loop if the user wants to end the schedule
            if source_id is None:
                break

            # retrieve the source from the source list
            source = None
            if isinstance(source_id, int) or source_id.isdigit():
                source = next(s for s in slot_sources if s.id == source_id)

            # allow new source
            if source_id == "BYURL":
                url = inquirer.text(
                    message="Source URL:",
                    **inqdef.markers(1),
                ).execute()

                source_type = SourceTypeDetector.determine_source_type(url)
                name = ".." + url[-30:] if len(url) > 30 else url

                match source_type:
                    case SourceType.LIVE:
                        name = "Live Source for VC: .." + name
                        (source, status) = obj.api.sources.live.upsert(
                            LiveSourceIn(name=name, url=url), if_exists="retrieve"
                        )
                        source_id = source.id
                    case SourceType.ASSET:
                        name = "Source Asset for VC: .." + name
                        (source, status) = obj.api.sources.asset.upsert(
                            AssetSourceIn(name=name, url=url), if_exists="retrieve"
                        )
                        source_id = source.id
                    case _:
                        click.secho(
                            f"Source type not supported in VCs: {source_type}",
                            fg="red",
                        )
                        source_id = "SKIP"

                if source:
                    click.secho(
                        f"     » Source {source.id}: {status.name.lower()}", fg="green"
                    )
                if source.format != vc.format:
                    click.secho(
                        f"     ! Source {source.id} has wrong format ({source.format} != {vc.format})",
                        fg="red",
                    )
                    source = None
                    source_id = "SKIP"

            # set default duration for valid sources
            if source_id == "ADBREAK":
                default_duration = adbreak_default_duration

            if source:
                if source.type == SourceType.LIVE:
                    default_duration = "10 min"
                else:
                    handler: ContentHandler = factory.create_handler(
                        source.full_url, user_agent=ConfigProvider().get_user_agent()
                    )
                    default_duration = str(handler.get_duration())

            if source_id != "SKIP":
                # ask for duration to insert
                duration = inquirer.text(
                    message="Duration",
                    default=default_duration,
                    **inqdef.markers(1),
                    filter=lambda t: parse_duration_expression(t),
                    transformer=lambda t: str(
                        timedelta(seconds=parse_duration_expression(t))
                    ),
                    long_instruction="Use a number (of seconds) or a duration expression (eg. 2h, 30m)",
                ).execute()

                if source_id == "ADBREAK":
                    adbreak_default_duration = str(duration)

                schedule.append(dict(source_id=source_id, duration=duration, start=t0))

                t0 += timedelta(seconds=duration)

        schedule_duration = sum([s["duration"] for s in schedule])

        click.echo()

        # Ask if slots are to be repeated
        if len(schedule):
            repeat = inquirer.number(
                message="How many times would you like to repeat this schedule?",
                default=1,
                min_allowed=1,
                max_allowed=20,
                filter=lambda i: int(i),
                **inqdef.markers(),
            ).execute()

            # Now create the slots
            slots = []
            for i in range(repeat):
                for sched in schedule:
                    if sched["source_id"] == "ADBREAK":
                        slot = VirtualChannelSlotIn(
                            startTime=sched["start"]
                            + timedelta(seconds=schedule_duration * i),
                            duration=sched["duration"],
                            type=VirtualChannelSlotType.AD_BREAK,
                        )
                    else:
                        slot = VirtualChannelSlotIn(
                            startTime=sched["start"]
                            + timedelta(seconds=schedule_duration * i),
                            duration=sched["duration"],
                            replacement=dict(id=sched["source_id"]),
                            type=VirtualChannelSlotType.CONTENT,
                        )
                    slot = api.slots.create(vc.id, slot)
                    slots.append(slot)

            obj.response_handler.treat_list_resources(
                slots,
                select_fields=[
                    "id",
                    "name",
                    "type",
                    "relativeStartTime",
                    "relativeEndTime",
                    "duration",
                    "replacement.id",
                    "replacement.name",
                ],
            )

    return populate
