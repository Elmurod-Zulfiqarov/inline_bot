import datetime

from django.utils import timezone
from telegram import ParseMode, Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CallbackContext
from telegram import ParseMode
from post.models import Posts


from tgbot.handlers.onboarding import static_text
from tgbot.handlers.utils.info import extract_user_data_from_update
from tgbot.models import User
from tgbot.handlers.onboarding.keyboards import make_keyboard_for_start_command


def command_start(update: Update, context: CallbackContext) -> None:
	u, created = User.get_user_and_created(update, context)

	if created:
		text = static_text.start_created.format(first_name=u.first_name)
	else:
		text = static_text.start_not_created.format(first_name=u.first_name)
	text += "\nBu inline bot. @clc_py_bot ...(search) qilib ko'rishingiz mumkin!"
	update.message.reply_text(text=text)


def inline_query(update: Update, context: CallbackContext) -> None:
	query = update.inline_query.query

	if query == "":
		return

	results = [
		InlineQueryResultArticle(
			id=post.id,
			title=post.title,
			description=post.content,
			thumb_url = post.image,
			thumb_width = 5,
			thumb_height = 5,
			input_message_content=InputTextMessageContent(f"{post.title}\n{post.image}", parse_mode=None),
		) for post in Posts.objects.filter(title__icontains=query)]
		
	update.inline_query.answer(results)



def secret_level(update: Update, context: CallbackContext) -> None:
	# callback_data: SECRET_LEVEL_BUTTON variable from manage_data.py
	""" Pressed 'secret_level_button_text' after /start command"""
	user_id = extract_user_data_from_update(update)['user_id']
	text = static_text.unlock_secret_room.format(
		user_count=User.objects.count(),
		active_24=User.objects.filter(updated_at__gte=timezone.now() - datetime.timedelta(hours=24)).count()
	)

	context.bot.edit_message_text(
		text=text,
		chat_id=user_id,
		message_id=update.callback_query.message.message_id,
		parse_mode=ParseMode.HTML
	)
