"""
This type stub file was generated by pyright.
"""

import discord
from typing import Any, Callable, Dict, Final, Iterable, List, Literal, NamedTuple, Optional, TYPE_CHECKING, Union
from . import ReactionButton, ReactionMenu, ViewMenu
from enum import Enum
from .abc import _BaseButton

"""
MIT License

Copyright (c) 2021-present @defxult

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
DEALINGS IN THE SOFTWARE.
"""
if TYPE_CHECKING:
	...
class _Details(NamedTuple):
	"""Used for buttons with a `custom_id` of `ID_CALLER`"""
	func: Callable[..., None]
	args: Iterable[Any]
	kwargs: Dict[str, Any]
	...


Details = _Details
class ViewButton(discord.ui.Button, _BaseButton):
	"""A helper class for :class:`ViewMenu`. Represents a UI button.
	
	Parameters
	----------
	style: :class:`discord.ButtonStyle`
		The style of the button
	
	label: Optional[:class:`str`]
		The button label, if any
	
	disabled: :class:`bool`
		Whether the button is disabled or not
	
	custom_id: Optional[:class:`str`]
		The ID of the button that gets received during an interaction. If this button is for a URL, it does not have a custom ID
	
	url: Optional[:class:`str`]
		The URL this button sends you to
	
	emoji: Optional[Union[:class:`str`, :class:`discord.PartialEmoji`]]
		The emoji of the button, if available
	
	followup: Optional[:class:`ViewButton.Follow`]
		Used with buttons with custom_id :attr:`ViewButton.ID_CALLER`, :attr:`ViewButton.ID_SEND_MESSAGE`, :attr:`ViewButton.ID_CUSTOM_EMBED`
	
	event: Optional[:class:`ViewButton.Event`]
		Set the button to be disabled or removed when it has been pressed a certain amount of times
	
	Kwargs
	------
	name: :class:`str`
		An optional name for the button. Can be set to retrieve it later via :meth:`ViewMenu.get_button()`
	
	skip: :class:`ViewButton.Skip`
		Set the action and the amount of pages to skip when using a `custom_id` of `ViewButton.ID_SKIP`
	
	persist: :class:`bool`
		Available only when using link buttons. This prevents link buttons from being disabled/removed when the menu times out or is stopped so they can remain clickable
	
		.. added v3.1.0
			:param:`persist`
	"""
	ID_NEXT_PAGE: Final[str] = ...
	ID_PREVIOUS_PAGE: Final[str] = ...
	ID_GO_TO_FIRST_PAGE: Final[str] = ...
	ID_GO_TO_LAST_PAGE: Final[str] = ...
	ID_GO_TO_PAGE: Final[str] = ...
	ID_END_SESSION: Final[str] = ...
	ID_CALLER: Final[str] = ...
	ID_SEND_MESSAGE: Final[str] = ...
	ID_CUSTOM_EMBED: Final[str] = ...
	ID_SKIP: Final[str] = ...
	_RE_IDs = ...
	_RE_UNIQUE_ID_SET = ...
	def __init__(self, *, style: discord.ButtonStyle = ..., label: Optional[str] = ..., disabled: bool = ..., custom_id: Optional[str] = ..., url: Optional[str] = ..., emoji: Optional[Union[str, discord.PartialEmoji]] = ..., followup: Optional[ViewButton.Followup] = ..., event: Optional[ViewButton.Event] = ..., **kwargs) -> None:
		...
	
	def __repr__(self): # -> str:
		...
	
	async def callback(self, interaction: discord.Interaction) -> None:
		"""*INTERNAL USE ONLY* - The callback function from the button interaction. This should not be manually called"""
		...
	
	class Followup:
		"""A class that represents the message sent using a :class:`ViewButton`. Contains parameters similar to method `discord.abc.Messageable.send`. Only to be used with :class:`ViewButton` kwarg "followup".
		It is to be noted that this should not be used with :class:`ViewButton` with a "style" of `discord.ButtonStyle.link` because link buttons do not send interaction events.
		
		Parameters
		----------
		content: Optional[:class:`str`]
			Message to send
		
		embed: Optional[:class:`discord.Embed`]
			Embed to send. Can also bet set for buttons with a custom_id of :attr:`ViewButton.ID_CUSTOM_EMBED`
		
		file: Optional[:class:`discord.File`]
			File to send. If the :class:`ViewButton` custom_id is :attr:`ViewButton.ID_SEND_MESSAGE`, the file will be ignored because of discord API limitations
		
		tts: :class:`bool`
			If discord should read the message aloud. Not valid for `ephemeral` messages
		
		allowed_mentions: Optional[:class:`discord.AllowedMentions`]
			Controls the mentions being processed in the menu message. Not valid for `ephemeral` messages
		
		delete_after: Optional[Union[:class:`int`, :class:`float`]]
			Amount of time to wait before the message is deleted. Not valid for `ephemeral` messages
		
		ephemeral: :class:`bool`
			If the message will be hidden from everyone except the person that pressed the button. This is only valid for a :class:`ViewButton` with custom_id :attr:`ViewButton.ID_SEND_MESSAGE`
		
		Kwargs
		------
		details: :meth:`ViewButton.Followup.set_caller_details()`
			The information that will be used when a `ViewButton.ID_CALLER` button is pressed (defaults to :class:`None`)
		"""
		__slots__ = ...
		def __repr__(self): # -> LiteralString:
			...
		
		def __init__(self, content: Optional[str] = ..., *, embed: Optional[discord.Embed] = ..., file: Optional[discord.File] = ..., tts: bool = ..., allowed_mentions: Optional[discord.AllowedMentions] = ..., delete_after: Optional[Union[int, float]] = ..., ephemeral: bool = ..., **kwargs) -> None:
			...
		
		@staticmethod
		def set_caller_details(func: Callable[..., None], *args, **kwargs) -> Details:
			"""|static method|
			
			Set the parameters for the function you set for a :class:`ViewButton` with the custom_id :attr:`ViewButton.ID_CALLER`
			
			Parameters
			----------
			func: Callable[..., :class:`None`]
				The function object that will be called when the associated button is pressed
			
			*args: `Any`
				An argument list that represents the parameters of that function
			
			**kwargs: `Any`
				An argument list that represents the kwarg parameters of that function
			
			Returns
			-------
			:class:`Details`: The :class:`NamedTuple` containing the values needed to internally call the function you have set
			
			Raises
			------
			- `IncorrectType`: Parameter "func" was not a callable object
			"""
			...
		
	
	
	@property
	def menu(self) -> Optional[ViewMenu]:
		"""
		Returns
		-------
		Optional[:class:`ViewMenu`]: The menu instance this button is attached to. Could be :class:`None` if the button is not attached to a menu
		"""
		...
	
	@classmethod
	def generate_skip(cls, label: str, action: Literal['+', '-'], amount: int) -> ViewButton:
		"""|class method|
		
		A factory method that returns a :class:`ViewButton` with the following parameters set:
		
		- style: `discord.ButtonStyle.gray`
		- label: `<label>`
		- custom_id: :attr:`ViewButton.ID_SKIP`
		- skip: `ViewButton.Skip(<action>, <amount>)`
		"""
		...
	
	@classmethod
	def link(cls, label: str, url: str) -> ViewButton:
		"""|class method|
		
		A factory method that returns a :class:`ViewButton` with the following parameters set:
		
		- style: `discord.ButtonStyle.link`
		- label: `<label>`
		- url: `<url>`
		"""
		...
	
	@classmethod
	def back(cls) -> ViewButton:
		"""|class method|
		
		A factory method that returns a :class:`ViewButton` with the following parameters set:
		
		- style: `discord.ButtonStyle.gray`
		- label: "Back"
		- custom_id: :attr:`ViewButton.ID_PREVIOUS_PAGE`
		"""
		...
	
	@classmethod
	def next(cls) -> ViewButton:
		"""|class method|
		
		A factory method that returns a :class:`ViewButton` with the following parameters set:
		
		- style: `discord.ButtonStyle.gray`
		- label: "Next"
		- custom_id: :attr:`ViewButton.ID_NEXT_PAGE`
		"""
		...
	
	@classmethod
	def go_to_first_page(cls) -> ViewButton:
		"""|class method|
		
		A factory method that returns a :class:`ViewButton` with the following parameters set:
		
		- style: `discord.ButtonStyle.gray`
		- label: "First Page"
		- custom_id: :attr:`ViewButton.ID_GO_TO_FIRST_PAGE`
		"""
		...
	
	@classmethod
	def go_to_last_page(cls) -> ViewButton:
		"""|class method|
		
		A factory method that returns a :class:`ViewButton` with the following parameters set:
		
		- style: `discord.ButtonStyle.gray`
		- label: "Last Page"
		- custom_id: :attr:`ViewButton.ID_GO_TO_LAST_PAGE`
		"""
		...
	
	@classmethod
	def go_to_page(cls) -> ViewButton:
		"""|class method|
		
		A factory method that returns a :class:`ViewButton` with the following parameters set:
		
		- style: `discord.ButtonStyle.gray`
		- label: "Page Selection"
		- custom_id: :attr:`ViewButton.ID_GO_TO_PAGE`
		"""
		...
	
	@classmethod
	def end_session(cls) -> ViewButton:
		"""|class method|
		
		A factory method that returns a :class:`ViewButton` with the following parameters set:
		
		- style: `discord.ButtonStyle.gray`
		- label: "Close"
		- custom_id: :attr:`ViewButton.ID_END_SESSION`
		"""
		...
	
	@classmethod
	def all(cls) -> List[ViewButton]:
		"""|class method|
		
		A factory method that returns a list of all base navigation buttons. The following buttons are returned with pre-set values:
		
		- Button 1
			- style: `discord.ButtonStyle.gray`
			- label: "First Page"
			- custom_id: :attr:`ViewButton.ID_GO_TO_FIRST_PAGE`
		- Button 2
			- style: `discord.ButtonStyle.gray`
			- label: "Back"
			- custom_id: :attr:`ViewButton.ID_PREVIOUS_PAGE`
		- Button 3
			- style: `discord.ButtonStyle.gray`
			- label: "Next"
			- custom_id: :attr:`ViewButton.ID_NEXT_PAGE`
		- Button 4
			- style: `discord.ButtonStyle.gray`
			- label: "Last Page"
			- custom_id: :attr:`ViewButton.ID_GO_TO_LAST_PAGE`
		- Button 5
			- style: `discord.ButtonStyle.gray`
			- label: "Page Selection"
			- custom_id: :attr:`ViewButton.ID_GO_TO_PAGE`
		- Button 6
			- style: `discord.ButtonStyle.gray`
			- label: "Close"
			- custom_id: :attr:`ViewButton.ID_END_SESSION`

		They are returned in that order
		
		Returns
		-------
		List[:class:`ViewButton`]
		"""
		...
	
	@classmethod
	def all_with_emojis(cls) -> List[ViewButton]:
		"""|class method|
		
		A factory method that returns a list of all base navigation buttons with emojis assigned instead of labels. The following buttons are returned with pre-set values:
		
		- Button 1
			- style: `discord.ButtonStyle.gray`
			- emoji: ⏪
			- custom_id: :attr:`ViewButton.ID_GO_TO_FIRST_PAGE`
		- Button 2
			- style: `discord.ButtonStyle.gray`
			- emoji: ◀️
			- custom_id: :attr:`ViewButton.ID_PREVIOUS_PAGE`
		- Button 3
			- style: `discord.ButtonStyle.gray`
			- emoji: ▶️
			- custom_id: :attr:`ViewButton.ID_NEXT_PAGE`
		- Button 4
			- style: `discord.ButtonStyle.gray`
			- emoji: ⏩
			- custom_id: :attr:`ViewButton.ID_GO_TO_LAST_PAGE`
		- Button 5
			- style: `discord.ButtonStyle.gray`
			- emoji: 🔢
			- custom_id: :attr:`ViewButton.ID_GO_TO_PAGE`
		- Button 6
			- style: `discord.ButtonStyle.gray`
			- emoji: ⏹️
			- custom_id: :attr:`ViewButton.ID_END_SESSION`

		They are returned in that order
		
		Returns
		-------
		List[:class:`ViewButton`]

			.. added:: v3.1.0
		"""
		...
	


class ButtonType(Enum):
	"""A helper class for :class:`ReactionMenu`. Determines the generic action a button can perform."""
	NEXT_PAGE = ...
	PREVIOUS_PAGE = ...
	GO_TO_FIRST_PAGE = ...
	GO_TO_LAST_PAGE = ...
	GO_TO_PAGE = ...
	END_SESSION = ...
	CUSTOM_EMBED = ...
	CALLER = ...
	SKIP = ...


class ReactionButton(_BaseButton):
	"""A helper class for :class:`ReactionMenu`. Represents a reaction.
	
	Parameters
	----------
	emoji: :class:`str`
		The discord reaction that will be used

	linked_to: :class:`ReactionButton.Type`
		A generic action a button can perform
	
	Kwargs
	------
	embed: :class:`discord.Embed`
		Only used when :param:`linked_to` is set as :attr:`ReactionButton.Type.CUSTOM_EMBED`. This is the embed that can be selected separately from the menu (`TypeEmbed` menu's only)

	name: :class:`str`
		An optional name for the button. Can be set to retrieve it later via :meth:`ReactionMenu.get_button()`

	details: :meth:`ReactionButton.set_caller_details()`
		The class method used to set the function and it's arguments to be called when the button is pressed
	
	event: :class:`ReactionButton.Event`
		Determine when a button should be removed depending on how many times it has been pressed

	skip: :class:`ReactionButton.Skip`
		Set the action and the amount of pages to skip when using a `linked_to` of `ReactionButton.Type.SKIP`
	"""
	Type = ButtonType
	def __init__(self, *, emoji: str, linked_to: ReactionButton.Type, **kwargs) -> None:
		...
	
	def __str__(self) -> str:
		...
	
	def __repr__(self): # -> str:
		...
	
	@property
	def menu(self) -> Optional[ReactionMenu]:
		"""
		Returns
		-------
		Optional[:class:`ReactionMenu`]: The menu the button is currently operating under. Can be :class:`None` if the button is not registered to a menu
		"""
		...
	
	@staticmethod
	def set_caller_details(func: Callable[..., None], *args, **kwargs) -> Details:
		"""|static method|
		
		Set the parameters for the function you set for a :class:`ReactionButton` with a `linked_to` of :attr:`ReactionButton.Type.CALLER`

		Parameters
		----------
		func: Callable[..., :class:`None`]
			The function object that will be called when the associated button is pressed
		
		*args: `Any`
			An argument list that represents the parameters of that function
		
		**kwargs: `Any`
			An argument list that represents the kwarg parameters of that function
		
		Returns
		-------
		:class:`Details`: The :class:`NamedTuple` containing the values needed to internally call the function you have set
		
		Raises
		------
		- `IncorrectType`: Parameter "func" was not a callable object
		"""
		...
	
	@classmethod
	def generate_skip(cls, emoji: str, action: Literal['+', '-'], amount: int) -> ReactionButton:
		"""|class method|
		
		A factory method that returns a :class:`ReactionButton` with the following parameters set:
		
		- emoji: `<emoji>`
		- linked_to: :attr:`ReactionButton.Type.SKIP`
		- skip: `ReactionButton.Skip(<action>, <amount>)`
		"""
		...
	
	@classmethod
	def back(cls) -> ReactionButton:
		"""|class method|
		
		A factory method that returns a :class:`ReactionButton` with the following parameters set:
		
		- emoji: ◀️
		- linked_to: :attr:`ReactionButton.Type.PREVIOUS_PAGE`
		"""
		...
	
	@classmethod
	def next(cls) -> ReactionButton:
		"""|class method|
		
		A factory method that returns a :class:`ReactionButton` with the following parameters set:
		
		- emoji: ▶️
		- linked_to: :attr:`ReactionButton.Type.NEXT_PAGE`
		"""
		...
	
	@classmethod
	def go_to_first_page(cls) -> ReactionButton:
		"""|class method|
		
		A factory method that returns a :class:`ReactionButton` with the following parameters set:
		
		- emoji: ⏪
		- linked_to: :attr:`ReactionButton.Type.GO_TO_FIRST_PAGE`
		"""
		...
	
	@classmethod
	def go_to_last_page(cls) -> ReactionButton:
		"""|class method|
		
		A factory method that returns a :class:`ReactionButton` with the following parameters set:
		
		- emoji: ⏩
		- linked_to: :attr:`ReactionButton.Type.GO_TO_LAST_PAGE`
		"""
		...
	
	@classmethod
	def go_to_page(cls) -> ReactionButton:
		"""|class method|
		
		A factory method that returns a :class:`ReactionButton` with the following parameters set:
		
		- emoji: 🔢
		- linked_to: :attr:`ReactionButton.Type.GO_TO_PAGE`
		"""
		...
	
	@classmethod
	def end_session(cls) -> ReactionButton:
		"""|class method|
		
		A factory method that returns a :class:`ReactionButton` with the following parameters set:
		
		- emoji: ⏹️
		- linked_to: :attr:`ReactionButton.Type.END_SESSION`
		"""
		...
	
	@classmethod
	def all(cls) -> List[ReactionButton]:
		"""|class method|
		
		A factory method that returns a `list` of all base navigation buttons. Base navigation buttons are :class:`ReactionButton` with a `linked_to` of:
		
		- :attr:`ReactionButton.Type.GO_TO_FIRST_PAGE`
		- :attr:`ReactionButton.Type.PREVIOUS_PAGE`
		- :attr:`ReactionButton.Type.NEXT_PAGE`
		- :attr:`ReactionButton.Type.GO_TO_LAST_PAGE`
		- :attr:`ReactionButton.Type.GO_TO_PAGE`
		- :attr:`ReactionButton.Type.END_SESSION`

		They are returned in that order
		"""
		...
	

