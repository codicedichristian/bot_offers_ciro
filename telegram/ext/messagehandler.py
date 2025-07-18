#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2020
# Leandro Toledo de Souza <devs@python-telegram-bot.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].

"""This module contains the MessageHandler class."""
import warnings

from telegram.utils.deprecate import TelegramDeprecationWarning

from telegram import Update
from telegram.ext import Filters
from .handler import Handler


class MessageHandler(Handler):
    """Handler class to handle telegram messages. They might contain text, media or status updates.

    Attributes:
        filters (:obj:`Filter`): Only allow updates with these Filters. See
            :mod:`telegram.ext.filters` for a full list of all available filters.
        callback (:obj:`callable`): The callback function for this handler.
        pass_update_queue (:obj:`bool`): Determines whether ``update_queue`` will be
            passed to the callback function.
        pass_job_queue (:obj:`bool`): Determines whether ``job_queue`` will be passed to
            the callback function.
        pass_user_data (:obj:`bool`): Determines whether ``user_data`` will be passed to
            the callback function.
        pass_chat_data (:obj:`bool`): Determines whether ``chat_data`` will be passed to
            the callback function.
        message_updates (:obj:`bool`): Should "normal" message updates be handled?
            Default is ``None``.
        channel_post_updates (:obj:`bool`): Should channel posts updates be handled?
            Default is ``None``.
        edited_updates (:obj:`bool`): Should "edited" message updates be handled?
            Default is ``None``.

    Note:
        :attr:`pass_user_data` and :attr:`pass_chat_data` determine whether a ``dict`` you
        can use to keep any data in will be sent to the :attr:`callback` function. Related to
        either the user or the chat that the update was sent in. For each update from the same user
        or in the same chat, it will be the same ``dict``.

        Note that this is DEPRECATED, and you should use context based callbacks. See
        https://git.io/fxJuV for more info.

    Args:
        filters (:class:`telegram.ext.BaseFilter`, optional): A filter inheriting from
            :class:`telegram.ext.filters.BaseFilter`. Standard filters can be found in
            :class:`telegram.ext.filters.Filters`. Filters can be combined using bitwise
            operators (& for and, | for or, ~ for not). Default is
            :attr:`telegram.ext.filters.Filters.update`. This defaults to all message_type updates
            being: ``message``, ``edited_message``, ``channel_post`` and ``edited_channel_post``.
            If you don't want or need any of those pass ``~Filters.update.*`` in the filter
            argument.
        callback (:obj:`callable`): The callback function for this handler. Will be called when
            :attr:`check_update` has determined that an update should be processed by this handler.
            Callback signature for context based API:

            ``def callback(update: Update, context: CallbackContext)``

            The return value of the callback is usually ignored except for the special case of
            :class:`telegram.ext.ConversationHandler`.
        pass_update_queue (:obj:`bool`, optional): If set to ``True``, a keyword argument called
            ``update_queue`` will be passed to the callback function. It will be the ``Queue``
            instance used by the :class:`telegram.ext.Updater` and :class:`telegram.ext.Dispatcher`
            that contains new updates which can be used to insert updates. Default is ``False``.
            DEPRECATED: Please switch to context based callbacks.
        pass_job_queue (:obj:`bool`, optional): If set to ``True``, a keyword argument called
            ``job_queue`` will be passed to the callback function. It will be a
            :class:`telegram.ext.JobQueue` instance created by the :class:`telegram.ext.Updater`
            which can be used to schedule new jobs. Default is ``False``.
            DEPRECATED: Please switch to context based callbacks.
        pass_user_data (:obj:`bool`, optional): If set to ``True``, a keyword argument called
            ``user_data`` will be passed to the callback function. Default is ``False``.
            DEPRECATED: Please switch to context based callbacks.
        pass_chat_data (:obj:`bool`, optional): If set to ``True``, a keyword argument called
            ``chat_data`` will be passed to the callback function. Default is ``False``.
            DEPRECATED: Please switch to context based callbacks.
        message_updates (:obj:`bool`, optional): Should "normal" message updates be handled?
            Default is ``None``.
            DEPRECATED: Please switch to filters for update filtering.
        channel_post_updates (:obj:`bool`, optional): Should channel posts updates be handled?
            Default is ``None``.
            DEPRECATED: Please switch to filters for update filtering.
        edited_updates (:obj:`bool`, optional): Should "edited" message updates be handled? Default
            is ``None``.
            DEPRECATED: Please switch to filters for update filtering.

    Raises:
        ValueError

    """

    def __init__(self,
                 filters,
                 callback,
                 pass_update_queue=False,
                 pass_job_queue=False,
                 pass_user_data=False,
                 pass_chat_data=False,
                 message_updates=None,
                 channel_post_updates=None,
                 edited_updates=None):

        super(MessageHandler, self).__init__(
            callback,
            pass_update_queue=pass_update_queue,
            pass_job_queue=pass_job_queue,
            pass_user_data=pass_user_data,
            pass_chat_data=pass_chat_data)
        if message_updates is False and channel_post_updates is False and edited_updates is False:
            raise ValueError(
                'message_updates, channel_post_updates and edited_updates are all False')
        self.filters = filters
        if self.filters is not None:
            self.filters &= Filters.update
        else:
            self.filters = Filters.update
        if message_updates is not None:
            warnings.warn('message_updates is deprecated. See https://git.io/fxJuV for more info',
                          TelegramDeprecationWarning,
                          stacklevel=2)
            if message_updates is False:
                self.filters &= ~Filters.update.message

        if channel_post_updates is not None:
            warnings.warn('channel_post_updates is deprecated. See https://git.io/fxJuV '
                          'for more info',
                          TelegramDeprecationWarning,
                          stacklevel=2)
            if channel_post_updates is False:
                self.filters &= ~Filters.update.channel_post

        if edited_updates is not None:
            warnings.warn('edited_updates is deprecated. See https://git.io/fxJuV for more info',
                          TelegramDeprecationWarning,
                          stacklevel=2)
            if edited_updates is False:
                self.filters &= ~(Filters.update.edited_message
                                  | Filters.update.edited_channel_post)

    def check_update(self, update):
        """Determines whether an update should be passed to this handlers :attr:`callback`.

        Args:
            update (:class:`telegram.Update`): Incoming telegram update.

        Returns:
            :obj:`bool`

        """
        if isinstance(update, Update) and update.effective_message:
            return self.filters(update)

    def collect_additional_context(self, context, update, dispatcher, check_result):
        if isinstance(check_result, dict):
            context.update(check_result)
