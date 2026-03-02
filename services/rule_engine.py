def apply_platform_rules(platform, caption):

    if platform == "twitter":
        return caption[:280]

    if platform == "instagram":
        return caption + "\n\n#trending #viral #content"

    if platform == "linkedin":
        return caption.replace("🔥", "")

    return caption