# مولّد العرض التقديمي

يبني عرضاً بصيغة `.pptx` عن النظام، بلقطات حقيقية مأخوذة من `index.html`
نفسه — لا صور مرسومة يدوياً، فلا يتقادم العرض عن المنتج.

## لماذا الشرائح صور

العرض عربي بالكامل. تصييره في Chromium يضمن تشكيل الحروف واتجاه النص
والخط نفسه المستعمل في المنتج (IBM Plex Sans Arabic) على أي جهاز يُفتح
عليه الملف. لو كُتب نصاً داخل PowerPoint لاستبدل الخط وأعاد لفّ السطور.
ملاحظات المُقدِّم تبقى نصاً حقيقياً في كل شريحة.

## التشغيل

```bash
cd tools/deck
npm install pptxgenjs playwright        # مرة واحدة
node shoot.js      # يلتقط لقطات النظام (حاسب ٢x وهاتف ٣x)
node check.js      # يتحقق أن لا شيء يتجاوز حدود الشريحة — يفشل إن تجاوز
node render.js     # يصيّر كل شريحة إلى PNG بدقة 3840x2160
node build.js      # يجمّعها في ملف .pptx مع ملاحظات المقدّم
```

`check.js` هو ما يمنع الخطأ الشائع: لقطة أطول من المساحة المتاحة تُقصّ
عند حافة الشريحة. يفحص كل عنصر هندسياً بدل الاعتماد على النظر.

## الخطوط

يحتاج `fonts/` بخطوط IBM Plex Sans Arabic وInter — تُنزَّل من Google Fonts.
والشعار يُستخرج من الحزمة نفسها:

```bash
python3 -c "import sys,json,base64; sys.path.insert(0,'../'); import bundle; \
  man=json.loads(bundle.section(bundle.read('../../index.html'),'manifest')[2]); \
  [open('assets/etihad-logo.png','wb').write(base64.b64decode(v['data'])) \
   for k,v in man.items() if v.get('mime')=='image/png']"
```

لون العلامة `#051C4A` مأخوذ من الشعار نفسه بالقياس، لا بالتقدير.
