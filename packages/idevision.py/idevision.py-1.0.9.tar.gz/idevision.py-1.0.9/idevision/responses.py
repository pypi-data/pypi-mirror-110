import datetime

class idevisionresponse:
    pass

class RTFMResponse(idevisionresponse):
    def __init__(self, nodes, response_time):
        self.nodes=nodes
        self.response_time=float(response_time)

    def __str__(self):
        return f"<RTFMResponse nodes={self.nodes} response_time={self.response_time}>"

class RTFSResponse(idevisionresponse):
    def __init__(self, nodes, response_time):
        self.nodes=nodes
        self.response_time=float(response_time)

    def __str__(self):
        return f"<RTFSResponse nodes={self.nodes} response_time={self.response_time}>"

class XKCDComic(idevisionresponse):
    def __init__(self, number, posted, safe_title, title, alt, transcript, news, image_url, url):
        self.number = number
        
        self.posted = datetime.datetime.strptime(posted, "%Y-%m-%dT%H:%M:%S")

        self.safe_title = safe_title
        self.title = title

        self.alt_text = alt

        self.transcript = transcript

        self.news = news

        self.image_url = image_url
        self.url = url

    def __str__(self):
        return f"<XKCDComic number={self.number} posted={datetime.datetime.strftime(self.posted, '%Y-%m-%dT%H:%M:%S')} safe_title={self.safe_title} title={self.title} alt_text={self.alt_text} transcript={self.transcript} news={self.news} image_url={self.image_url} url={self.url}>"

class XKCDResponse(idevisionresponse):
    def __init__(self, nodes, query_time):
        self.nodes = nodes

        self.query_time = query_time

    def __str__(self):
        return f"<xkcd nodes={[str(node) for node in self.nodes]} query_time={self.query_time}>"
    
class CDNResponse(idevisionresponse):
    def __init__(self, url, slug, node):
        self.url = url
        self.slug = slug
        self.node = node
    
    def __str__(self):
        return f"{self.slug} at {self.url} on node {self.node}"
    
class CDNStats(idevisionresponse):
    def __init__(self, upload_count, uploaded_today, last_uploaded):
        self.upload_count = upload_count
        self.uploaded_today = uploaded_today
        
        self.last_uploaded = last_uploaded
        
    def __str__(self):
        return f"<CDNStats upload_count={self.upload_count} uploaded_today={self.uploaded_today} last_uploaded={self.last_uploaded}>"
    
class CDNUpload(idevisionresponse):
    def __init__(self, url, timestamp, author, views, node, size, expiry):
        self.url = url
        self.timestamp = datetime.datetime.fromtimestamp(timestamp)
        self.author = author
        self.views = views
        self.node = node
        self.size = size
        self.expiry = expiry
        
    def __str__(self):
        return f"<CDNUpload url={self.url} timestamp={self.timestamp} author={self.author} views={self.views} node={self.node} size={self.size} expiry={self.expiry}>"