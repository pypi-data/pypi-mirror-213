# -*- coding: utf-8 -*-

from mod.common.component.baseComponent import BaseComponent

class ChatExtensionComponentServer(BaseComponent):
    def Enable(self):
        # type: () -> bool
        """
        启用官方聊天扩展功能。需要在ClientLoadAddonsFinishServerEvent事件中调用。仅在联机大厅和网络服中生效。
        """
        pass

    def Disable(self):
        # type: () -> bool
        """
        关闭官方聊天扩展功能。需要在ClientLoadAddonsFinishServerEvent事件中调用。仅在联机大厅和网络服中生效。
        """
        pass

    def RegisterChatPrefix(self, prefix, prefixColor):
        # type: (str, str) -> bool
        """
        为游戏内指定玩家注册聊天前缀。仅在主界面消息框和聊天界面游戏频道生效。建议在AddServerPlayerEvent事件中调用，为新玩家添加前缀。
        """
        pass

    def SetShowSocialNearbyInfo(self, show):
        # type: (bool) -> bool
        """
        设置是否显示官方聊天社交界面中同一游戏玩家是否在附近信息。
        """
        pass

