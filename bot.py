import logging
import random
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes, MessageHandler, filters
)

TOKEN = "8506658443:AAHCv82zVYDBR0D0JW4BSbWNt75RwChfVd0"

logging.basicConfig(level=logging.INFO)

# ═══════════════════════════════════════
# 600 SO'Z — 30 UNIT
# ═══════════════════════════════════════
UNITS = {
1: [("afraid","qo'rqqan"),("agree","rozi bo'lmoq"),("angry","g'azablangan"),("arrive","yetib kelmoq"),("attack","hujum qilmoq"),("bottom","tag, pastki qism"),("clever","aqlli"),("cruel","shafqatsiz"),("finally","va nihoyat"),("hide","yashirinmoq"),("hunt","ov qilmoq"),("lot","juda ko'p"),("middle","o'rta"),("moment","lahza"),("pleased","xursand"),("promise","va'da bermoq"),("reply","javob bermoq"),("safe","xavfsiz"),("trick","hiyla"),("well","yaxshi")],
2: [("adventure","sarguzasht"),("approach","yaqinlashmoq"),("carefully","ehtiyotkorlik bilan"),("chemical","kimyoviy modda"),("create","yaratmoq"),("evil","yovuz"),("experiment","tajriba"),("kill","o'ldirmoq"),("laboratory","laboratoriya"),("laugh","kulmoq"),("loud","shovqinli"),("nervous","xavotirlangan"),("noise","shovqin"),("project","loyiha"),("scare","qo'rqitmoq"),("secret","sir"),("shout","baqirmoq"),("smell","hidlamoq"),("terrible","dahshatli"),("worse","yomonroq")],
3: [("alien","o'zga sayyoralik"),("among","orasida"),("chart","jadval"),("cloud","bulut"),("comprehend","tushunmoq"),("describe","tasvirlamoq"),("ever","hech qachon"),("fail","muvaffaqiyatsiz bo'lmoq"),("friendly","do'stona"),("grade","baho"),("instead","o'rniga"),("library","kutubxona"),("planet","sayyora"),("report","hisobot"),("several","bir nechta"),("solve","yechmoq"),("suddenly","to'satdan"),("suppose","faraz qilmoq"),("universe","koinot"),("view","manzara")],
4: [("appropriate","mos, to'g'ri"),("avoid","qochmoq"),("behave","odob saqlamoq"),("calm","xotirjam"),("concern","tashvish"),("content","qoniqgan"),("expect","kutmoq"),("frequently","tez-tez"),("habit","odat"),("instruct","o'rgatmoq"),("issue","masala"),("none","hech biri"),("patient","sabrli"),("positive","ijobiy"),("punish","jazolash"),("represent","ifodalash"),("shake","silkitmoq"),("spread","tarqalmoq"),("stroll","sayr qilmoq"),("village","qishloq")],
5: [("aware","xabardor"),("badly","yomon"),("belong","tegishli bo'lmoq"),("continue","davom ettirmoq"),("error","xato"),("experience","tajriba"),("field","dala, soha"),("hurt","og'riq"),("judgment","hukm"),("likely","ehtimoliy"),("normal","oddiy"),("rare","noyob"),("relax","dam olmoq"),("request","so'rov"),("reside","yashash"),("result","natija"),("roll","aylanmoq"),("since","chunki"),("visible","ko'rinadigan"),("wild","yovvoyi")],
6: [("advantage","afzallik"),("cause","sabab"),("choice","tanlov"),("community","jamoa"),("dead","o'lik"),("distance","masofa"),("escape","qochmoq"),("face","yuz"),("follow","ergashmoq"),("fright","qo'rquv"),("ghost","arvoh"),("individual","shaxs"),("pet","uy hayvoni"),("reach","yetmoq"),("return","qaytmoq"),("survive","omon qolmoq"),("upset","xafa"),("voice","ovoz"),("weather","ob-havo"),("wise","dono")],
7: [("allow","ruxsat bermoq"),("announce","e'lon qilmoq"),("beside","yonida"),("challenge","sinov"),("claim","da'vo qilmoq"),("condition","holat"),("contribute","hissa qo'shmoq"),("difference","farq"),("divide","bo'lmoq"),("expert","mutaxassis"),("famous","mashhur"),("force","kuch"),("harm","zarar"),("lay","yotqizmoq"),("peace","tinchlik"),("prince","shahzoda"),("protect","himoya qilmoq"),("sense","his"),("sudden","to'satdan"),("therefore","shuning uchun")],
8: [("accept","qabul qilmoq"),("arrange","tartiblamoq"),("attend","qatnashmoq"),("balance","muvozanat"),("contrast","qarama-qarshi"),("encourage","rag'batlantirmoq"),("familiar","tanish"),("grab","ushlamoq"),("hang","osmoq"),("huge","ulkan"),("necessary","zarur"),("pattern","namuna"),("propose","taklif qilmoq"),("purpose","maqsad"),("release","ozod qilmoq"),("require","talab qilmoq"),("single","yagona"),("success","muvaffaqiyat"),("tear","ko'z yoshi"),("theory","nazariya")],
9: [("against","qarshi"),("beach","qirg'oq"),("damage","zarar"),("discover","kashf etmoq"),("emotion","his-tuyg'u"),("fix","tuzatmoq"),("frank","samimiy"),("identify","aniqlash"),("island","orol"),("ocean","okean"),("perhaps","balki"),("pleasant","yoqimli"),("prevent","oldini olmoq"),("rock","tosh"),("save","qutqarmoq"),("step","qadam"),("still","hali ham"),("taste","ta'm"),("throw","uloqtirmoq"),("wave","to'lqin")],
10: [("benefit","foyda"),("certain","aniq"),("chance","imkoniyat"),("effect","ta'sir"),("essential","zarur, asosiy"),("far","uzoq"),("focus","diqqat jamlash"),("function","vazifa"),("grass","o't"),("guard","qorovul"),("image","tasvir"),("immediate","darhol"),("primary","asosiy"),("proud","g'ururli"),("remain","qolmoq"),("rest","dam olmoq"),("separate","ajratmoq"),("site","joy, manzil"),("tail","dum"),("trouble","muammo")],
11: [("anymore","endi"),("asleep","uxlab yotgan"),("berry","rezavor"),("collect","to'plamoq"),("compete","raqobat qilmoq"),("conversation","suhbat"),("creature","jonivor"),("decision","qaror"),("either","yoki"),("forest","o'rmon"),("ground","yer, zamin"),("introduce","tanishtirmoq"),("marry","uylanmoq"),("prepare","tayyorlamoq"),("sail","suzmoq"),("serious","jiddiy"),("spend","sarflamoq"),("strange","g'alati"),("truth","haqiqat"),("wake","uyg'onmoq")],
12: [("alone","yolg'iz"),("apartment","kvartira"),("article","maqola"),("artist","rassom"),("attitude","munosabat"),("compare","taqqoslash"),("judge","sudya"),("magazine","jurnal"),("material","material"),("meal","ovqat"),("method","usul"),("neighbor","qo'shni"),("professional","mutaxassis"),("profit","foyda"),("quality","sifat"),("shape","shakl"),("space","fazo"),("stair","zinapoya"),("symbol","ramz"),("thin","ingichka")],
13: [("blood","qon"),("burn","yonmoq"),("cell","hujayra"),("contain","o'z ichiga olmoq"),("correct","to'g'ri"),("crop","hosil"),("demand","talab qilmoq"),("equal","teng"),("feed","boqmoq"),("hole","teshik"),("increase","ko'paymoq"),("lord","xo'jayin"),("owe","qarzdor bo'lmoq"),("position","lavozim"),("raise","ko'tarmoq"),("responsible","mas'ul"),("sight","ko'rish"),("spot","nuqta, joy"),("structure","tuzilma"),("whole","butun")],
14: [("coach","murabbiy"),("control","boshqarmoq"),("description","tavsif"),("direct","to'g'ridan-to'g'ri"),("exam","imtihon"),("example","misol"),("limit","chegara"),("local","mahalliy"),("magical","sehrli"),("mail","pochta"),("novel","roman"),("outline","reja"),("poet","shoir"),("print","bosmoq"),("scene","sahna"),("sheet","varaq"),("silly","ahmoq"),("store","do'kon"),("suffer","azob chekmoq"),("technology","texnologiya")],
15: [("across","orqali"),("breathe","nafas olmoq"),("characteristic","xususiyat"),("consume","iste'mol qilmoq"),("excite","hayajontirmoq"),("extreme","haddan tashqari"),("fear","qo'rquv"),("fortunate","baxtli"),("happen","sodir bo'lmoq"),("length","uzunlik"),("mistake","xato"),("observe","kuzatmoq"),("opportunity","imkoniyat"),("prize","mukofot"),("race","poyga"),("realize","anglamoq"),("respond","javob bermoq"),("risk","xavf"),("wonder","hayron bo'lmoq"),("yet","hali")],
16: [("academy","akademiya"),("ancient","qadimiy"),("board","kengash"),("century","asr"),("clue","ipuci"),("concert","konsert"),("county","tuman"),("dictionary","lug'at"),("exist","mavjud bo'lmoq"),("flat","tekis, kvartira"),("gentleman","janob"),("hidden","yashirin"),("maybe","balki"),("officer","amaldor"),("original","asl"),("pound","funt"),("process","jarayon"),("publish","nashr etmoq"),("theater","teatr"),("wealth","boylik")],
17: [("appreciate","qadrlamoq"),("available","mavjud"),("beat","urmoq"),("bright","yorqin"),("celebrate","nishonlamoq"),("determine","aniqlash"),("disappear","yo'qolmoq"),("else","boshqa"),("fair","adolatli"),("flow","oqmoq"),("forward","oldinga"),("hill","tepalik"),("level","daraja"),("lone","yolg'iz"),("puddle","ko'lmak"),("response","javob"),("season","fasl"),("solution","yechim"),("waste","isrof"),("whether","yoki")],
18: [("argue","bahslashmoq"),("communicate","muloqot qilmoq"),("crowd","olomon"),("depend","bog'liq bo'lmoq"),("dish","idish"),("empty","bo'sh"),("exact","aniq"),("fresh","yangi, toza"),("gather","to'plamoq"),("indicate","ko'rsatmoq"),("item","buyum"),("offer","taklif etmoq"),("price","narx"),("product","mahsulot"),("property","mulk"),("purchase","sotib olmoq"),("recommend","tavsiya etmoq"),("select","tanlash"),("tool","asbob"),("treat","muomala qilmoq")],
19: [("alive","tirik"),("bone","suyak"),("bother","bezovta qilmoq"),("captain","kapitan"),("conclusion","xulosa"),("doubt","shubha"),("explore","kashf etmoq"),("foreign","chet el"),("glad","xursand"),("however","biroq"),("injustice","adolatsizlik"),("international","xalqaro"),("lawyer","advokat"),("mention","eslatmoq"),("policy","siyosat"),("social","ijtimoiy"),("speech","nutq"),("staff","xodimlar"),("toward","tomon"),("wood","yog'och")],
20: [("achieve","erishmoq"),("advise","maslahat bermoq"),("already","allaqachon"),("basic","asosiy"),("bit","biroz"),("consider","o'ylash"),("destroy","yo'q qilmoq"),("entertain","ko'ngil ochar"),("extra","qo'shimcha"),("goal","maqsad"),("lie","yolg'on gapirmoq"),("meat","go'sht"),("opinion","fikr"),("real","haqiqiy"),("reflect","aks ettirmoq"),("regard","hurmat"),("serve","xizmat qilmoq"),("vegetable","sabzavot"),("war","urush"),("worth","qadrli")],
21: [("appear","paydo bo'lmoq"),("base","asos"),("brain","miya"),("career","martaba"),("clerk","kotib"),("effort","urinish"),("enter","kirmoq"),("excellent","a'lo"),("hero","qahramon"),("hurry","shoshilmoq"),("inform","xabar bermoq"),("later","keyinroq"),("leave","ketmoq"),("locate","joylashmoq"),("nurse","hamshira"),("operation","operatsiya"),("pain","og'riq"),("refuse","rad etmoq"),("though","garchi"),("various","turli")],
22: [("actual","haqiqiy"),("amaze","hayron qoldirmoq"),("charge","haq olmoq"),("comfort","qulaylik"),("contact","aloqa"),("customer","mijoz"),("deliver","yetkazib bermoq"),("earn","ishlab topmoq"),("gate","darvoza"),("include","kiritmoq"),("manage","boshqarmoq"),("mystery","sir"),("occur","sodir bo'lmoq"),("opposite","teskari"),("plate","tarelka"),("receive","olmoq"),("reward","mukofot"),("set","o'rnatmoq"),("steal","o'g'irlamoq"),("thief","o'g'ri")],
23: [("advance","ilgarilamoq"),("athlete","sportchi"),("average","o'rtacha"),("behavior","xulq-atvor"),("behind","orqasida"),("course","kurs"),("lower","pastroq"),("match","musobaqa"),("member","a'zo"),("mental","aqliy"),("passenger","yo'lovchi"),("personality","shaxsiyat"),("poem","she'r"),("pole","qutb"),("remove","olib tashlash"),("safety","xavfsizlik"),("shoot","otmoq"),("sound","tovush"),("swim","suzmoq"),("web","to'r")],
24: [("block","to'smoq"),("cheer","quvvatlamoq"),("complex","murakkab"),("critic","tanqidchi"),("event","voqea"),("exercise","mashq"),("fit","mos kelmoq"),("friendship","do'stlik"),("guide","yo'l-yo'riq"),("lack","etishmasligi"),("passage","o'tish"),("perform","bajarmoq"),("pressure","bosim"),("probable","ehtimoliy"),("public","ommaviy"),("strike","zarba"),("support","qo'llab-quvvatlamoq"),("task","vazifa"),("term","atama"),("unite","birlashmoq")],
25: [("associate","hamkor"),("environment","atrof-muhit"),("factory","zavod"),("feature","xususiyat"),("instance","misol"),("involve","jalb etmoq"),("medicine","dori"),("mix","aralashtirmoq"),("organize","tashkil qilmoq"),("period","davr"),("populate","aholi bilan to'ldirmoq"),("produce","ishlab chiqarmoq"),("range","qator"),("recognize","tanib olmoq"),("regular","muntazam"),("sign","belgi"),("tip","maslahat"),("tradition","an'ana"),("trash","chiqindi"),("wide","keng")],
26: [("advice","maslahat"),("along","bo'ylab"),("attention","diqqat"),("attract","jalb etmoq"),("climb","chiqmoq"),("drop","tushirmoq"),("final","yakuniy"),("further","yanada"),("imply","anglatmoq"),("maintain","saqlamoq"),("neither","na...na"),("otherwise","aks holda"),("physical","jismoniy"),("prove","isbotlamoq"),("react","munosabat bildirmoq"),("ride","minmoq"),("situated","joylashgan"),("society","jamiyat"),("standard","standart"),("suggest","taklif qilmoq")],
27: [("actually","aslida"),("bite","tishlash"),("coast","sohil"),("deal","bitim"),("desert","cho'l"),("earthquake","zilzila"),("effective","samarali"),("examine","tekshirmoq"),("false","yolg'on"),("gift","sovg'a"),("hunger","ochlik"),("imagine","tasavvur qilmoq"),("journey","sayohat"),("puzzle","jumboq"),("quite","juda"),("rather","biroz"),("specific","aniq"),("tour","tur"),("trip","safar"),("value","qiymat")],
28: [("band","guruh"),("barely","zo'rg'a"),("boring","zerikarli"),("cancel","bekor qilmoq"),("driveway","kirish yo'li"),("garbage","chiqindi"),("instrument","asbob"),("list","ro'yxat"),("magic","sehr"),("message","xabar"),("notice","sezmoq"),("own","o'z"),("predict","bashorat qilmoq"),("professor","professor"),("rush","shoshilmoq"),("schedule","jadval"),("share","ulashmoq"),("stage","bosqich"),("storm","bo'ron"),("within","ichida")],
29: [("advertise","reklama qilmoq"),("assign","tayinlamoq"),("audience","tomoshabinlar"),("breakfast","nonushta"),("competition","musobaqa"),("cool","salqin"),("gain","qozonmoq"),("importance","ahamiyat"),("knowledge","bilim"),("major","asosiy"),("mean","anglatmoq"),("prefer","afzal ko'rmoq"),("president","prezident"),("progress","taraqqiyot"),("respect","hurmat"),("rich","boy"),("skill","mahorat"),("somehow","qandaydir"),("strength","kuch"),("vote","ovoz bermoq")],
30: [("above","ustida"),("ahead","oldinda"),("amount","miqdor"),("belief","ishonch"),("center","markaz"),("common","umumiy"),("cost","narx"),("demonstrate","ko'rsatmoq"),("different","farqli"),("evidence","dalil"),("honesty","halollik"),("idiom","iborat"),("independent","mustaqil"),("inside","ichida"),("master","usta"),("memory","xotira"),("proper","to'g'ri"),("scan","ko'zdan kechirmoq"),("section","bo'lim"),("surface","yuza")],
}

# ═══════════════════════════════════════
# DATABASE (xotira ichida)
# ═══════════════════════════════════════
users = {}      # user_id -> {name, total_score, tests, correct, wrong}
sessions = {}   # user_id -> {unit, questions, cur, score, correct, wrong}

def get_user(uid, name):
    if uid not in users:
        users[uid] = {"name": name, "total_score": 0, "tests": 0, "correct": 0, "wrong": 0}
    return users[uid]

# ═══════════════════════════════════════
# KEYBOARDS
# ═══════════════════════════════════════
def main_menu_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📚 Unit tanlash", callback_data="units")],
        [InlineKeyboardButton("📊 Statistika", callback_data="stats"),
         InlineKeyboardButton("🏆 Reyting", callback_data="rating")],
        [InlineKeyboardButton("ℹ️ Yordam", callback_data="help")],
    ])

def units_kb(page=0):
    rows = []
    start = page * 10 + 1
    end = min(start + 9, 30)
    row = []
    for i in range(start, end + 1):
        row.append(InlineKeyboardButton(f"📖 {i}", callback_data=f"unit_{i}"))
        if len(row) == 5:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton("⬅️ 1-10", callback_data="units_page_0"))
    if end < 30:
        nav.append(InlineKeyboardButton("11-30 ➡️", callback_data="units_page_1"))
    if nav:
        rows.append(nav)
    rows.append([InlineKeyboardButton("🏠 Bosh sahifa", callback_data="home")])
    return InlineKeyboardMarkup(rows)

def options_kb(options, q_idx):
    rows = []
    letters = ["🅰️ A", "🅱️ B", "🇨 C", "🇩 D"]
    for i, opt in enumerate(options):
        rows.append([InlineKeyboardButton(f"{letters[i]}: {opt}", callback_data=f"ans_{q_idx}_{i}")])
    rows.append([InlineKeyboardButton("⛔ Testni tugatish", callback_data="end_test")])
    return InlineKeyboardMarkup(rows)

def after_answer_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➡️ Keyingisi", callback_data="next_q")]
    ])

def result_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Qayta o'ynash", callback_data="retry")],
        [InlineKeyboardButton("📚 Boshqa unit", callback_data="units")],
        [InlineKeyboardButton("🏠 Bosh sahifa", callback_data="home")],
    ])

# ═══════════════════════════════════════
# HANDLERS
# ═══════════════════════════════════════
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    get_user(user.id, user.first_name)
    text = (
        f"👋 Salom, *{user.first_name}*\\!\n\n"
        "📚 *4000 Essential English Words*\n"
        "Bu bot sizga inglizcha so'zlarni test orqali o'rgatadi\\.\n\n"
        "🎯 *30 unit* — har birida *20 ta so'z*\n"
        "✅ To'g'ri javob — *+1 ball*\n"
        "🏆 Reyting va statistika mavjud\\!\n\n"
        "Quyidagi menyudan tanlang:"
    )
    await update.message.reply_text(text, parse_mode="MarkdownV2", reply_markup=main_menu_kb())

async def button(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    name = q.from_user.first_name
    data = q.data

    # HOME
    if data == "home":
        text = (
            f"🏠 *Bosh sahifa*\n\n"
            f"Salom, *{name}*\\! Nima qilmoqchisiz?"
        )
        await q.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=main_menu_kb())

    # UNITS LIST
    elif data == "units" or data.startswith("units_page_"):
        page = 0
        if data.startswith("units_page_"):
            page = int(data.split("_")[-1])
        text = (
            "📚 *Unit tanlang*\n\n"
            "Har bir unitda 20 ta so'z bor\\.\n"
            "Unit raqamini bosing va test boshlang\\!"
        )
        await q.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=units_kb(page))

    # UNIT START
    elif data.startswith("unit_"):
        unit_num = int(data.split("_")[1])
        await start_test(q, uid, name, unit_num)

    # RETRY
    elif data == "retry":
        if uid in sessions:
            unit_num = sessions[uid]["unit"]
            await start_test(q, uid, name, unit_num)
        else:
            await q.edit_message_text("❌ Avval unit tanlang.", reply_markup=units_kb())

    # ANSWER
    elif data.startswith("ans_"):
        parts = data.split("_")
        q_idx = int(parts[1])
        chosen = int(parts[2])
        await handle_answer(q, uid, q_idx, chosen)

    # NEXT QUESTION
    elif data == "next_q":
        await send_question(q, uid)

    # END TEST
    elif data == "end_test":
        await show_result(q, uid)

    # STATS
    elif data == "stats":
        u = get_user(uid, name)
        acc = round(u["correct"] / max(u["correct"] + u["wrong"], 1) * 100)
        text = (
            f"📊 *Mening statistikam*\n\n"
            f"👤 Ism: *{escape_md(u['name'])}*\n"
            f"💰 Jami ball: *{u['total_score']}*\n"
            f"📝 Testlar: *{u['tests']}*\n"
            f"✅ To'g'ri javoblar: *{u['correct']}*\n"
            f"❌ Noto'g'ri: *{u['wrong']}*\n"
            f"🎯 Aniqlik: *{acc}%*"
        )
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Bosh sahifa", callback_data="home")]])
        await q.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=kb)

    # RATING
    elif data == "rating":
        sorted_users = sorted(users.items(), key=lambda x: x[1]["total_score"], reverse=True)[:20]
        medals = ["🥇", "🥈", "🥉"]
        lines = ["🌍 *Umumiy reyting \\(Top 20\\)*\n"]
        for i, (u_id, u_data) in enumerate(sorted_users):
            medal = medals[i] if i < 3 else f"{i+1}\\."
            me = " ← Siz" if u_id == uid else ""
            lines.append(f"{medal} *{escape_md(u_data['name'])}* — {u_data['total_score']} ball{escape_md(me)}")
        text = "\n".join(lines)
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Bosh sahifa", callback_data="home")]])
        await q.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=kb)

    # HELP
    elif data == "help":
        text = (
            "ℹ️ *Yordam*\n\n"
            "📚 *Qanday ishlaydi?*\n"
            "1\\. Unit tanlaysiz \\(1\\-30\\)\n"
            "2\\. 20 ta savol beriladi\n"
            "3\\. 4 ta variantdan birini tanlaysiz\n"
            "4\\. To'g'ri javob ✅ yoki xato ❌ ko'rsatiladi\n"
            "5\\. Test oxirida natija chiqadi\n\n"
            "🏆 *Ball tizimi:*\n"
            "• To'g'ri javob: \\+1 ball\n"
            "• Xato javob: 0 ball\n\n"
            "📊 Statistika va reyting mavjud\\!"
        )
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Bosh sahifa", callback_data="home")]])
        await q.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=kb)

# ═══════════════════════════════════════
# TEST LOGIC
# ═══════════════════════════════════════
async def start_test(q, uid, name, unit_num):
    get_user(uid, name)
    words = list(UNITS[unit_num])
    random.shuffle(words)
    sessions[uid] = {
        "unit": unit_num,
        "questions": words,
        "cur": 0,
        "score": 0,
        "correct": 0,
        "wrong": 0,
    }
    text = (
        f"🚀 *Unit {unit_num} — Test boshlandi\\!*\n\n"
        f"📝 20 ta savol\n"
        f"✅ To'g'ri javob \\= \\+1 ball\n\n"
        f"Tayyor bo'lsangiz, birinchi savol\\!"
    )
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("▶️ Boshlash!", callback_data="next_q")]])
    await q.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=kb)

async def send_question(q, uid):
    if uid not in sessions:
        await q.edit_message_text("❌ Session topilmadi. /start bosing.", reply_markup=main_menu_kb())
        return

    s = sessions[uid]
    if s["cur"] >= len(s["questions"]):
        await show_result(q, uid)
        return

    word, correct_uz = s["questions"][s["cur"]]
    unit_num = s["unit"]
    all_words = UNITS[unit_num]

    # 4 ta variant yasash
    wrong_pool = [uz for en, uz in all_words if uz != correct_uz]
    wrongs = random.sample(wrong_pool, min(3, len(wrong_pool)))
    options = wrongs + [correct_uz]
    random.shuffle(options)

    correct_idx = options.index(correct_uz)
    s["current_correct"] = correct_idx
    s["current_options"] = options

    cur = s["cur"]
    total = len(s["questions"])
    score = s["score"]
    prog = "▓" * (cur * 10 // total) + "░" * (10 - cur * 10 // total)

    text = (
        f"📖 *Unit {unit_num}* \\| {cur+1}/{total}\n"
        f"{escape_md(prog)} *{score} ball*\n\n"
        f"🔤 So'z:\n"
        f"━━━━━━━━━━━━━━\n"
        f"**{escape_md(word.upper())}**\n"
        f"━━━━━━━━━━━━━━\n\n"
        f"O'zbekcha tarjimasini toping:"
    )
    await q.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=options_kb(options, cur))

async def handle_answer(q, uid, q_idx, chosen_idx):
    if uid not in sessions:
        return
    s = sessions[uid]
    if s["cur"] != q_idx:
        return

    correct_idx = s.get("current_correct", -1)
    options = s.get("current_options", [])
    word, correct_uz = s["questions"][s["cur"]]

    if chosen_idx == correct_idx:
        s["score"] += 1
        s["correct"] += 1
        result_line = f"✅ *To'g'ri\\!* \\+1 ball"
        emoji = random.choice(["🎉", "🌟", "💪", "🔥", "👏"])
    else:
        s["wrong"] += 1
        chosen_txt = escape_md(options[chosen_idx]) if chosen_idx < len(options) else "?"
        result_line = f"❌ *Xato\\!*\nSiz: {chosen_txt}\nTo'g'ri: *{escape_md(correct_uz)}*"
        emoji = "😅"

    s["cur"] += 1
    remaining = len(s["questions"]) - s["cur"]
    cur = s["cur"]
    total = len(s["questions"])
    prog = "▓" * (cur * 10 // total) + "░" * (10 - cur * 10 // total)

    text = (
        f"{emoji} *{escape_md(word.upper())}*\n\n"
        f"{result_line}\n\n"
        f"{escape_md(prog)} {cur}/{total} \\| *{s['score']} ball*"
    )

    if s["cur"] >= total:
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("📊 Natijani ko'rish", callback_data="end_test")]])
    else:
        kb = after_answer_kb()

    await q.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=kb)

async def show_result(q, uid):
    if uid not in sessions:
        await q.edit_message_text("🏠 Bosh sahifa", reply_markup=main_menu_kb())
        return

    s = sessions[uid]
    total = len(s["questions"])
    score = s["score"]
    correct = s["correct"]
    wrong = s["wrong"]
    unit_num = s["unit"]
    pct = round(score / max(total, 1) * 100)

    u = users.get(uid, {})
    u["total_score"] = u.get("total_score", 0) + score
    u["tests"] = u.get("tests", 0) + 1
    u["correct"] = u.get("correct", 0) + correct
    u["wrong"] = u.get("wrong", 0) + wrong

    if pct >= 90:
        emoji, grade = "🏆", "Mukammal\\!"
    elif pct >= 75:
        emoji, grade = "🌟", "Juda yaxshi\\!"
    elif pct >= 60:
        emoji, grade = "👍", "Yaxshi\\!"
    elif pct >= 40:
        emoji, grade = "💪", "Davom eting\\!"
    else:
        emoji, grade = "😅", "Ko'proq mashq qiling\\!"

    bar = "▓" * (pct // 10) + "░" * (10 - pct // 10)

    text = (
        f"{emoji} *Unit {unit_num} — Natija*\n\n"
        f"*{grade}*\n\n"
        f"{escape_md(bar)} *{pct}%*\n\n"
        f"✅ To'g'ri: *{correct}/{total}*\n"
        f"❌ Xato: *{wrong}/{total}*\n"
        f"💰 Ball: *\\+{score}*\n"
        f"📈 Jami ballingiz: *{u['total_score']}*"
    )

    del sessions[uid]
    await q.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=result_kb())

def escape_md(text):
    """Telegram MarkdownV2 uchun maxsus belgilarni ekranlash"""
    text = str(text)
    chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for c in chars:
        text = text.replace(c, f'\\{c}')
    return text

# ═══════════════════════════════════════
# MAIN
# ═══════════════════════════════════════
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    print("✅ Bot ishga tushdi!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
