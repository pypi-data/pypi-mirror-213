import threefive


def summarize(payload):
    cue = threefive.Cue(payload)
    cue.decode()

    lines = []
    match cue.info_section.splice_command_type:
        case 5:
            lines.append(
                "payload: cmd_type='{}' ({}), event_id={}, duration={}, avail={}/{}".format(
                    cue.command.name,
                    cue.command.command_type,
                    cue.command.splice_event_id,
                    cue.command.break_duration,
                    cue.command.avail_num,
                    cue.command.avail_expected,
                )
            )
        case 6:
            lines.append(
                "payload: cmd_type='{}' ({})".format(
                    cue.command.name,
                    cue.command.command_type,
                )
            )

    for d in cue.descriptors:
        if d.tag != 0:
            lines.append(
                "descriptor: '{}' ({}), event_id: {}{dur}{upid}{pos}".format(
                    d.segmentation_message or "(Unknown)",
                    d.segmentation_type_id,
                    int(d.segmentation_event_id, 16),
                    dur=f", duration:{d.segmentation_duration}"
                    if d.segmentation_duration_flag
                    else "",
                    upid=f", upid:{d.segmentation_upid['private_data']}"
                    if d.segmentation_upid
                    else "",
                    pos="segment: {}/{}".format(d.segment_num, d.segments_expected)
                    if hasattr(d, "segments_expected")
                    else "",
                )
            )

    return lines
