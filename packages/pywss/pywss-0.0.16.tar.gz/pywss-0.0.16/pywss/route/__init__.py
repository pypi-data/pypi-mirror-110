# coding: utf-8
import re
import loggus

from pywss.handlers.static import newStaticHandler
from pywss.handlers.websocket import WebSocketHandler


class _RouteMap:

    def __init__(self):
        self.__staticRouteMap = {}
        self.__dynamicRouteList = []
        self.__staticDirRouteList = []

    def register(self, route, *handlers):
        if "(?P<" in route:
            regex = re.sub("(\?P<.*?>)\)", "\\1[^/?]*?)", route) + "/?$"
            prefix = re.search("(.*?)\(\?P", route).group(1)
            length = route.count("/")
            self.__dynamicRouteList.append((prefix, length, re.compile(regex).match, handlers))
        else:
            self.__staticRouteMap[route] = handlers

    def registerStaticDir(self, route, *handlers):
        self.__staticDirRouteList.append((route, handlers))

    def search(self, route):
        inPath = f"{route.strip('/')}"
        if inPath in self.__staticRouteMap:
            return {}, self.__staticRouteMap[inPath], None
        for dirRoute, handlers in self.__staticDirRouteList:
            if inPath.startswith(dirRoute):
                return {"path": inPath.replace(dirRoute, "", 1)}, handlers, None
        inLength = inPath.count("/")
        for index in range(len(self.__dynamicRouteList)):
            prefix, length, match, handlers = self.__dynamicRouteList[index]
            if length == inLength and inPath.startswith(prefix):
                pathMatch = match(inPath)
                if pathMatch:
                    return pathMatch.groupdict(), handlers, None
        return None, None, "404 by pywss"


RouteMap = _RouteMap()


class Route:

    def __init__(self, route="", routeMap=RouteMap):
        self.route = f"/{route.strip().strip('/')}" if route else route
        self.routeMap = routeMap
        self.handlers = []
        self.log = loggus.withFields({"module": "Route", "party": route})

    def use(self, *handlers):
        self.handlers += list(handlers)

    def party(self, route, *handlers):
        if not route:
            self.use(*handlers)
            return self
        route = Route(f"{self.route}/{route.strip().strip('/')}")
        handlers = self.handlers + list(handlers)
        route.use(*handlers)
        return route

    def __register(self, method, route, *handlers):
        if not handlers:
            return self.log.withFields({"route": route}).warning(f"undefined handlers, ignore!")
        if not route:
            return self.log.withFields({"route": route}).warning(f"undefined route, ignore!")
        route = route.strip().strip("/")
        route = f"{method}{self.route}/{route}"
        handlers = self.handlers + list(handlers)
        self.routeMap.register(route, *handlers)

    def static(
            self, route, *handlers, root=".", method="GET",
            textHtml="html,txt",
            textCss="css",
            applicationXJavascript="js",
            applicationJson="json,yml,yaml",
            applicationXml="xml",
            imagePng="jpg,jpeg,png,gif",
            default="application/octet-stream",
    ):
        route = route.strip().strip("/")
        route = f"{method}{self.route}/{route}"
        handlers = self.handlers + list(handlers)
        handlers.append(newStaticHandler(
            root,
            textHtml=textHtml,
            textCss=textCss,
            applicationXJavascript=applicationXJavascript,
            applicationJson=applicationJson,
            applicationXml=applicationXml,
            imagePng=imagePng,
            default=default))
        self.routeMap.registerStaticDir(route, *handlers)

    def get(self, route, *handlers):
        self.__register("GET", route, *handlers)

    def head(self, route, *handlers):
        self.__register("HEAD", route, *handlers)

    def post(self, route, *handlers):
        self.__register("POST", route, *handlers)

    def put(self, route, *handlers):
        self.__register("PUT", route, *handlers)

    def delete(self, route, *handlers):
        self.__register("DELETE", route, *handlers)

    def options(self, route, *handlers):
        self.__register("OPTIONS", route, *handlers)

    def patch(self, route, *handlers):
        self.__register("PATCH", route, *handlers)

    def websocket(self, route, *handlers):
        route = route.strip().strip("/")
        route = f"GET{self.route}/{route}"
        handlers = [WebSocketHandler] + self.handlers + list(handlers)
        self.routeMap.register(route, *handlers)
