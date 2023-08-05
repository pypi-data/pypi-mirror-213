import click
import cloup
import InquirerPy.inquirer as inquirer
from bpkio_api.models import AdInsertionServiceIn, SourceType

import bpkio_cli.utils.inquirer as inqdef
from bpkio_cli.core.app_context import AppContext


def create_ad_insertion_service_command():
    # COMMAND: CREATE
    @cloup.command(help="Create a (simple) Ad Insertion service")
    @click.pass_obj
    def create(obj: AppContext):
        all_sources = obj.api.sources.list()

        # Ask for the source
        sources = [
            s
            for s in all_sources
            if s.type in (SourceType.LIVE, SourceType.ASSET_CATALOG)
        ]
        sources = sorted(sources, key=lambda s: s.id, reverse=True)
        sources = obj.cache.sort_resources_by_most_recently_accessed(sources)
        choices = [
            dict(value=s.id, name=f"({s.id})  {s.name}  [{s.type.value}]")
            for s in sources
        ]
        source_id = inquirer.fuzzy(
            message="Source", choices=choices, **inqdef.select_markers()
        ).execute()
        source_type = next(s for s in sources if s.id == source_id).type

        # Then ask for the ad server
        ad_sources = [s for s in all_sources if s.type == SourceType.AD_SERVER]
        ad_sources = sorted(ad_sources, key=lambda s: s.id, reverse=True)
        ad_sources = obj.cache.sort_resources_by_most_recently_accessed(ad_sources)
        choices = [dict(value=s.id, name=f"({s.id})  {s.name}") for s in ad_sources]
        ad_source_id = inquirer.fuzzy(
            message="Ad Server", choices=choices, **inqdef.select_markers()
        ).execute()

        # Then ask for the gap filler
        slate_sources = [s for s in all_sources if s.type == SourceType.SLATE]
        slate_sources = sorted(slate_sources, key=lambda s: s.id, reverse=True)
        slate_sources = obj.cache.sort_resources_by_most_recently_accessed(
            slate_sources
        )
        choices = [dict(value=s.id, name=f"({s.id})  {s.name}") for s in slate_sources]
        choices = [dict(value=None, name="-- No gap filler --")] + choices
        slate_source_id = inquirer.fuzzy(
            message="Gap Filler", choices=choices, **inqdef.select_markers()
        ).execute()

        # Ask for the type of ad insertion (optionally)
        if source_type in (SourceType.ASSET, SourceType.ASSET_CATALOG):
            insertion_type = "vodAdInsertion"
        else:
            choices = [
                dict(value="liveAdPreRoll", name="Live Pre-Roll"),
                dict(value="liveAdReplacement", name="Live Ad Replacment"),
            ]
            insertion_type = inquirer.select(
                message="Ad Insertion Type", choices=choices, **inqdef.select_markers()
            ).execute()

        # Ask for transcoding profile
        profiles = obj.api.transcoding_profiles.list()
        profiles = obj.cache.sort_resources_by_most_recently_accessed(profiles)
        choices = [dict(value=s.id, name=f"{s.name} ({s.id})") for s in profiles]
        # ... add a "none" one
        choices = [dict(value=None, name="-- No transcoding --")] + choices
        transcoding_profile_id = inquirer.fuzzy(
            message="Transcoding Profile", choices=choices, **inqdef.select_markers()
        ).execute()

        # Ask for other options
        with_transcoding = transcoding_profile_id is not None

        name = inquirer.text(
            message="Name for the service",
            validate=lambda result: len(result) > 0,
            invalid_message="The name cannot be empty.",
            **inqdef.markers(0),
        ).execute()

        # Create the service object
        service = AdInsertionServiceIn(
            name=name, source=dict(id=source_id), enableAdTranscoding=with_transcoding
        )
        ad_insertion = dict(adServer=dict(id=ad_source_id))
        if slate_source_id is not None:
            ad_insertion["gapFiller"] = dict(id=slate_source_id)

        setattr(
            service,
            insertion_type,
            ad_insertion,
        )
        if with_transcoding:
            # setattr(service, "transcodingProfile", dict(id=transcoding_profile_id))
            service.transcodingProfile = dict(id=transcoding_profile_id)

        service_out = obj.api.services.ad_insertion.create(service)

        obj.response_handler.treat_single_resource(service_out)

    return create
