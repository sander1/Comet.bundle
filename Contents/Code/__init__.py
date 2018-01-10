TITLE = 'Comet'
PREFIX = '/video/comet'
ICON = 'icon-default.jpg'
ART = 'art-default.jpg'

WATCH_LIVE_URL = 'http://www.comettv.com/watch-live/'
RE_VIDEO_URL = Regex('file:[ ]*"(https?:\/\/.+\.m3u8[^"]+)"')

####################################################################################################
def Start():

	HTTP.CacheTime = 0

	ObjectContainer.art = R(ART)
	ObjectContainer.title1 = TITLE

	VideoClipObject.art = R(ART)
	VideoClipObject.thumb = R(ICON)

####################################################################################################
@handler(PREFIX, TITLE, thumb=ICON, art=ART)
def MainMenu():

	oc = ObjectContainer()

	oc.add(CreateVideoClipObject(
		title = 'Watch Comet Live'
	))

	return oc

####################################################################################################
@route(PREFIX + '/createvideoclipobject', include_container=bool)
def CreateVideoClipObject(title, include_container=False, **kwargs):

	videoclip_obj = VideoClipObject(
		key = Callback(CreateVideoClipObject, title=title, include_container=True),
		rating_key = WATCH_LIVE_URL,
		title = title,
		items = [
			MediaObject(
				parts = [
					PartObject(key=HTTPLiveStreamURL(Callback(PlayVideo, url=WATCH_LIVE_URL)))
				],
				audio_channels = 2,
				optimized_for_streaming = True,
			)
		]
	)

	if include_container:
		return ObjectContainer(objects=[videoclip_obj])
	else:
		return videoclip_obj

####################################################################################################
@route(PREFIX + '/playvideo.m3u8')
@indirect
def PlayVideo(url, **kwargs):

	data = HTTP.Request(url).content
	video_url = RE_VIDEO_URL.search(data)

	if video_url:
		return IndirectResponse(VideoClipObject, key=HTTPLiveStreamURL(video_url.group(1)))
	else:
		raise Ex.MediaNotAvailable
