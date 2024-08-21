import asyncio
import nest_asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import logging
from datetime import datetime

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 机器人的介绍信息
intro_message = """
使用自助提卡系统请确保您的telegram是从AppStore或者官网下载!
 
网络上下载的中文版telegram是有病毒的,会自动替换您收到的地址
 
由于系统是自动生成地址,无法上传地址的二维码图片供您核对
 
同时谨防人为上传带图片地址的系统,本系统从未对外授权
 
如不确定,切勿提币,请联系客服核验!

项目了解/客服咨询请移步主频道：
https://t.me/xiaomubiaofa
"""

async def start(update: Update, context: CallbackContext) -> None:
    user_full_name = update.effective_user.full_name  # 获取用户全名
    user_id = update.effective_user.id  # 获取用户ID
    username = update.effective_user.username  # 获取用户名
    user_link = f"<a href='tg://user?id={user_id}'>{user_full_name}</a>"
    
    # 记录用户信息到日志
    logger.info(f"User {user_full_name} (ID: {user_id}, Username: @{username}) started the bot.")
    
    keyboard = [
        ['面值1000元1张', '面值1000元2张'],
        ['面值1000元5张', '提取卡密'],
        ['账单核对'],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)
    welcome_message = f"欢迎{user_link}!\n" + intro_message
    await update.message.reply_text(welcome_message, reply_markup=reply_markup, parse_mode='HTML')

async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    user_full_name = update.effective_user.full_name  # 获取用户全名
    user_id = update.effective_user.id  # 获取用户ID
    username = update.effective_user.username  # 获取用户名
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 获取当前时间

    # 记录用户信息和消息到日志
    logger.info(f"User {user_full_name} (ID: {user_id}, Username: @{username}) sent message: {user_message}")
    
    responses = {
        '面值1000元1张': f"""
中石化加油卡面值1000元1张
提货价860元=118 USDT
（美元升值，usdt汇率提升，单张卡售价调整为118U）
闲鱼回收价970元(后续回收价变动以闲鱼回收系统为准)。您将获得差价利润110元

USDT支付钱包地址(TRC20):

<code>TSuoJSdzTZEk81YNEvBjFdkhhv5hmn1WVV</code>

点击复制👆

提现地址根据IP范围随机推送，当前获取的提现地址有效期截止到您发送区块链交易ID并提取到卡密。超过3小时未提现，再次操作需重新获取提现地址。提现成功后，区块链ID在您提取卡密前一直有效，请妥善保管。
        """,
        '面值1000元2张': f"""
中石化加油卡面值1000元2张
提货价1700元=234USDT
（汇率实时变化、系统识别入账金额以234USDT为准） 
闲鱼回收价970元×2。您将获得差价利润240元 

USDT支付钱包地址(TRC20):

<code>TBTP8kekYupyqS9xmj2Gwwjn78ZnTzuEKo</code>

点击复制👆

温馨提示：获取地址请确保您的telegram下载自AppStore/官网/应用市场；而非网络下载的中文版telegram
        """,
        '面值1000元5张': f"""
中石化加油卡面值1000元5张
提货价4200元=578USDT
（汇率实时变化、系统识别入账金额以578USDT为准） 
闲鱼回收价970元×5。您将获得差价利润650元 

USDT支付钱包地址(TRC20):

<code>TMpTRx9WL9ccA5g9XDeQzh7UMofeCQMGVZ</code>

点击复制👆

温馨提示：获取地址请确保您的telegram下载自AppStore/官网/应用市场；而非网络下载的中文版telegram
        """,
        '提取卡密': "抱歉，机器人尚未识别到您提供的有效交易号/哈希值，请检查核对您发送的交易号/哈希值是否正确。\n\n温馨提示：您必须提币给系统生成的地址，系统才能识别提币订单里的区块链交易ID,请确保您的telegram下载自官方网站或者AppStore",
        '账单核对': f"您的账户: <a href='tg://user?id={user_id}'>{user_full_name}</a>\n截止: {current_time}\n累计提卡 0张\n\n最近五张卡号卡密如下：\n\n系统未查询到您近期的有效提卡账单"
    }

    response = responses.get(user_message, None)

    if response:
        # 添加底部按钮，上下排列
        keyboard = [
            [InlineKeyboardButton('人工客服', url='https://t.me/zshyk66888')],
            [InlineKeyboardButton('USDT购买教程--新人必看', url='https://t.me/ouyibianUDS')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(response, reply_markup=reply_markup, parse_mode='HTML')

async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('使用 /start 来开始。')

async def error(update: Update, context: CallbackContext) -> None:
    logger.warning('Update "%s" caused error "%s"', update, context.error)

async def main():
    # Apply nest_asyncio if you're in an environment where the event loop is already running
    nest_asyncio.apply()

    # 将令牌直接添加到代码中
    token = '6651456576:AAG1HYVYALr_mECXcgnmyI5iE8KbVJ_tWB0'
    
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error)

    await application.run_polling()

if __name__ == '__main__':
    # 在脚本中运行异步主函数
    asyncio.run(main())
