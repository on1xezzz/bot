import time
import random
import requests
from datetime import datetime, timedelta
import pytz

BOT_TOKEN = '7782887867:AAHBKS3nGoLlnzc4jXeTLOVtmikGXdFH8KE'
CHANNEL_ID = '-1002841531910'
OWNER_ID = 756428648
OFFSET = None
AUTO_POSTING = False

CURRENCY_PAIRS = [
    'EURUSD', 'AUDCHF', 'AUDUSD', 'CADCHF', 'EURGBP', 'GBPAUD', 'GBPJPY', 'GBPUSD',
    'USDJPY', 'USDCHF', 'EURCHF', 'AUDCAD', 'NZDUSD', 'EURJPY', 'CHFJPY', 'AUDJPY',
    'CADJPY', 'EURAUD', 'EURCAD', 'USDCNH', 'USDCAD', 'USDSGD',
    'USDTRY', 'USDMYR', 'USDTHB', 'USDEGP', 'USDARS', 'USDBRL', 'USDMXN',
    'USDPKR', 'USDIDR', 'USDBDT', 'YERUSD', 'LBPUSD', 'AEDCNY',
    'SARCNY', 'QARCNY', 'NGNUSD', 'USDPHP', 'USDVND', 'UAHUSD', 'USDCOP'
]

emoji_map = {
    'AUD': '🇦🇺', 'CHF': '🇨🇭', 'EUR': '🇪🇺', 'USD': '🇺🇸', 'GBP': '🇬🇧',
    'JPY': '🇯🇵', 'CAD': '🇨🇦', 'NZD': '🇳🇿', 'CNH': '🇨🇳', 'TRY': '🇹🇷',
    'MYR': '🇲🇾', 'THB': '🇹🇭', 'EGP': '🇪🇬', 'ARS': '🇦🇷', 'BRL': '🇧🇷',
    'MXN': '🇲🇽', 'PKR': '🇵🇰', 'IDR': '🇮🇩', 'BDT': '🇧🇩', 'YER': '🇾🇪',
    'LBP': '🇱🇧', 'AED': '🇦🇪', 'SAR': '🇸🇦', 'QAR': '🇶🇦', 'NGN': '🇳🇬',
    'PHP': '🇵🇭', 'VND': '🇻🇳', 'UAH': '🇺🇦', 'COP': '🇨🇴'
}

SIGNALS = ['BUY', 'SELL']
PHOTO_BUY = 'https://i.imgur.com/a/sNdCYu9.jpeg'
PHOTO_SELL = 'https://i.imgur.com/a/nfhSHDG.jpeg'

session_stats = {'plus': 0, 'minus': 0, 'total': 0}
weekly_stats = []

BG_TZ = pytz.timezone('Europe/Sofia')

def is_within_trading_hours():
    now = datetime.now(BG_TZ).time()
    return now >= datetime.strptime('12:00', '%H:%M').time() and now <= datetime.strptime('15:00', '%H:%M').time()

def is_end_of_session():
    now = datetime.now(BG_TZ).time()
    return now >= datetime.strptime('15:00', '%H:%M').time() and now <= datetime.strptime('15:01', '%H:%M').time()

def is_end_of_week():
    now = datetime.now(BG_TZ)
    return now.weekday() == 6 and now.time() >= datetime.strptime('15:01', '%H:%M').time()

def reset_daily_stats():
    global session_stats
    weekly_stats.append(session_stats.copy())
    session_stats = {'plus': 0, 'minus': 0, 'total': 0}

def send_photo_with_caption(chat_id, photo_url, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    data = {
        'chat_id': chat_id,
        'photo': photo_url,
        'caption': caption,
        'parse_mode': 'HTML'
    }
    requests.post(url, data=data)

def generate_signal():
    pair = random.choice(CURRENCY_PAIRS)
    signal = random.choice(SIGNALS)
    base, quote = pair[:3], pair[3:]
    base_flag = emoji_map.get(base, '')
    quote_flag = emoji_map.get(quote, '')
    timeframe = random.choice(['1м', '5м'])
    indicators = {
        'RSI': round(random.uniform(10, 90), 5),
        'MACD': round(random.uniform(-0.01, 0.01), 5),
        'ADX': round(random.uniform(10, 50), 5),
        'Stochastic': round(random.uniform(0, 100), 5),
        'CCI': round(random.uniform(-200, 200), 5),
        'Momentum': round(random.uniform(-0.01, 0.01), 5),
        'EMA20': round(random.uniform(0.5, 1.5), 5),
        'SMA20': round(random.uniform(0.5, 1.5), 5),
    }
    price = round(random.uniform(0.5, 1.5), 5)
    advice = random.choice([
        "Не търгувай, когато си ядосан или прекалено ентусиазиран.",
        "Винаги поставяй стоп лос.",
        "Не рискувай повече от 2% от капитала на една сделка.",
        "Анализирай новините преди да влезеш в сделка.",
        "Следвай тренда, избягвай търговия по време на консолидация."
    ])
    signal_icon = "📈" if signal == 'BUY' else "📉"
    text = (
        f"{base_flag}/{quote_flag} Валутна двойка: {base}/{quote}\n\n"
        f"📌 Сигнал: {signal} {signal_icon}\n"
        f"⏱️ Таймфрейм: {timeframe}\n"
        f"💵 Цена: {price}\n\n"
        f"🧮 Анализ на индикаторите:\n\n"
        f"🔴 RSI: {indicators['RSI']}\n"
        f"🔴 MACD: {indicators['MACD']}\n"
        f"🔴 ADX: {indicators['ADX']}\n"
        f"🔴 Stochastic: {indicators['Stochastic']}\n"
        f"🔴 CCI: {indicators['CCI']}\n"
        f"🔴 Momentum: {indicators['Momentum']}\n"
        f"🔴 EMA20: {indicators['EMA20']}\n"
        f"🔴 SMA20: {indicators['SMA20']}\n\n"
        f"💡 Съвет: {advice}"
    )
    is_profitable = random.choices([True, False], weights=[70, 30])[0]
    if is_profitable:
        session_stats['plus'] += 1
    else:
        session_stats['minus'] += 1
    session_stats['total'] += 1
    return signal, text, pair  # ← ДОБАВЛЕНО: возвращаем валютную пару

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
    requests.post(url, data=data)

def get_updates(offset):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {'timeout': 10, 'offset': offset}
    response = requests.get(url, params=params)
    return response.json()

def process_commands(updates):
    global AUTO_POSTING, OFFSET
    for update in updates.get('result', []):
        OFFSET = update['update_id'] + 1
        message = update.get('message', {})
        text = message.get('text', '')
        chat_id = message.get('chat', {}).get('id')
        user_id = message.get('from', {}).get('id')
        if user_id != OWNER_ID:
            continue
        if text == '/start':
            if AUTO_POSTING:
                send_message(chat_id, "⚠️ Автоматичното публикуване вече е активно.")
            else:
                AUTO_POSTING = True
                send_message(chat_id, "✅ Автоматичното публикуване е активирано.")
        elif text == '/stop':
            AUTO_POSTING = False
            send_message(chat_id, "⏹ Автоматичното публикуване е спряно.")
        elif text == '/status':
            status = "✅ АКТИВНО" if AUTO_POSTING else "❌ НЕАКТИВНО"
            send_message(chat_id, f"Състояние на публикуването: {status}")
        elif text == '/testpost':
            signal, signal_text, pair = generate_signal()
            send_pre_signal_warning(pair)
            time.sleep(30)
            photo_url = PHOTO_BUY if signal == 'BUY' else PHOTO_SELL
            send_photo_with_caption(CHANNEL_ID, photo_url, signal_text)
            send_message(chat_id, "✅ Тестовият сигнал беше изпратен успешно (с предупреждение преди него).")


# ← ДОБАВЛЕНО: Функция предварительного предупреждения
def send_pre_signal_warning(pair):
    base, quote = pair[:3], pair[3:]
    base_flag = emoji_map.get(base, '')
    quote_flag = emoji_map.get(quote, '')
    warning_text = (
        f"🔔 Подгответе се за валутната двойка {base_flag}/{quote_flag} {base}/{quote}\n\n"
        f"👀 Сигналът ще бъде след няколко секунди, бъдете готови!\n\n"
        f"❗️ Подгответе сума за вход съгласно риск мениджмънта – не повече от 2% от баланса ви."
    )
    send_message(CHANNEL_ID, warning_text)

def main():
    global OFFSET
    print("Ботът е стартиран...")
    counter = 0
    while True:
        try:
            updates = get_updates(OFFSET)
            process_commands(updates)
            if AUTO_POSTING and is_within_trading_hours():
                if counter >= 5:
                    signal, signal_text, pair = generate_signal()  # ← ДОБАВЛЕНО: получаем пару
                    send_pre_signal_warning(pair)  # ← ДОБАВЛЕНО
                    time.sleep(30)  # ← ДОБАВЛЕНО

                    photo_url = PHOTO_BUY if signal == 'BUY' else PHOTO_SELL
                    send_photo_with_caption(CHANNEL_ID, photo_url, signal_text)
                    counter = 0
                else:
                    counter += 1
            if is_end_of_session():
                report = (
                    f"\uD83D\uDCCA <b>Резултати от търговската сесия:</b>\n\n"
                    f"\uD83D\uDCC8 Успешни сделки: <b>{session_stats['plus']}</b>\n"
                    f"\uD83D\uDCC9 Неуспешни сделки: <b>{session_stats['minus']}</b>\n"
                    f"\uD83D\uDCCA Общо сигнали: <b>{session_stats['total']}</b>\n\n"
                    f"\uD83D\uDCAC Запомни: Дори най-добрите стратегии не гарантират 100% успех!"
                )
                send_message(CHANNEL_ID, report)
                reset_daily_stats()
            if is_end_of_week():
                total_plus = sum(day['plus'] for day in weekly_stats)
                total_minus = sum(day['minus'] for day in weekly_stats)
                total_signals = sum(day['total'] for day in weekly_stats)
                weekly_report = (
                    f"\uD83D\uDCC6 <b>Седмичен отчет:</b>\n\n"
                    f"\uD83D\uDCCB Търговски дни: <b>{len(weekly_stats)}</b>\n"
                    f"\uD83D\uDCC8 Успешни сделки: <b>{total_plus}</b>\n"
                    f"\uD83D\uDCC9 Неуспешни сделки: <b>{total_minus}</b>\n"
                    f"\uD83D\uDCCA Общо сигнали: <b>{total_signals}</b>\n\n"
                    f"\uD83D\uDCE2 Ако си следвал сигналите – сподели резултатите си!"
                )
                send_message(CHANNEL_ID, weekly_report)
                weekly_stats.clear()
            time.sleep(1)
        except Exception as e:
            print("Грешка:", e)
            time.sleep(5)

if __name__ == "__main__":
    main()
