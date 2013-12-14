BP_PLUGIN_PREFIX = "/photos/TheBigPicture"
PLUGIN_TITLE = "The Big Picture"
BP_RSS_FEED = "http://feeds.boston.com/boston/bigpicture/index"
NAMESPACES = {"pheedo": "http://www.pheedo.com/namespace/pheedo"}

ART = R("art-default.jpg")
ICON = R("icon-default.png")

NUM_PHOTOS_REGEX = Regex('(\d+) photos')

####################################################################################################
def Start():
    Plugin.AddViewGroup("ImageStream", viewMode="Pictures", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")

    ObjectContainer.art = ART
    ObjectContainer.title1 = PLUGIN_TITLE
    ObjectContainer.view_group = "InfoList"
    DirectoryObject.thumb = ICON


####################################################################################################
@handler(BP_PLUGIN_PREFIX, PLUGIN_TITLE)
def MainMenu():
    oc = ObjectContainer()
    feed = XML.ElementFromURL(BP_RSS_FEED)
    for item in feed.xpath("//rss//channel//item"):
        description = item.xpath(".//description")[0].text.replace('&gt;', '>').replace('&lt', '<')

        # If no thumb is provided, we can assume no photo is available. This has been found when a daily
        # post was not made, actually due to illness. :(
        try:
            thumb = HTML.ElementFromString(description).xpath(".//div[@class='bpImageTop']//img")[0].get('src')
        except:
            continue

        date = Datetime.ParseDate(item.xpath("./pubDate")[0].text)
        url = item.xpath("./guid")[0].text
        title = item.xpath("./title")[0].text

        try:
            num_photos = NUM_PHOTOS_REGEX.search(description).group(1)
            summary = "%s - %s Photos" % (date.strftime("%x"), num_photos)
        except:
            summary = "%s" % date.strftime("%x")

        oc.add(PhotoAlbumObject(url=url, title=title, thumb=thumb, originally_available_at=date, summary=summary))

    return oc