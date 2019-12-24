<h1 align="center">
	<img width="200" src="static/ganjoor.jpg" alt="Aur">
	<br>
	<br>
</h1>

<div dir="rtl">
	<h1>API ارتباط با سایت گنجور توسعه داده شده توسط فریمورک فلسک</h1>
</div>
<div dir="rtl">
	<h3>نصب روی سرور شخصی</h3>
</div>

<div dir="rtl">
	ابتدا دستور زیر را در خط فرمان وارد کنید:
</div>

`sudo pip install -r requirements.txt`
<br />

<div dir="rtl">
	سپس وارد دایرکتوری اصلی شده و دستور زیر را وارد کنید:
</div>

`python wsgi`
<br />

<div dir="rtl">
	<h3>نحوه استفاده از API</h3>
</div>

<div dir="rtl">
	<h4>بیوگرافی شاعر مدنظر</h4>
</div>

`http://127.0.0.1:5000/poet?id=POETID`
<br />

<div dir="rtl">
	<h4>لیست شاعران به همراه ID هایشان</h4>
</div>

`http://127.0.0.1:5000/poets`
<br />

<div dir="rtl">
	<h4>انتخاب شعر به صورت تصادفی</h4>
</div>

`http://127.0.0.1:5000/random`
<br />

<div dir="rtl">
	<h4>انتخاب شعر تصادفی از شاعری خاص</h4>
</div>

`http://127.0.0.1:5000/random/hafez`
<br />

<div dir="rtl">
	<h3>گلاسری شاعران</h3>
</div>

<div dir="rtl">
	برای دسترسی به نام شاعران کافی ست به این آدرس ریکوئست بزنید:
</div>

`http://host/glossary`
<br />
