<div align="center">

<img src="assets/cover.svg" width="100%" alt="GREEN ARMOR ACADEMY" />

# OPERATION DIRECTORY

### مختبر تدريبي خفيف لفهم Active Directory وتقييم إعداداته الأمنية

**إعداد وتطوير: JEHAD GHABEN**  
**GREEN ARMOR ACADEMY**

[English README](README.md) · [تاسك الطلاب](docs/STUDENT_TASK.md) · [البنية التقنية](docs/ARCHITECTURE.md)

</div>

---

## ما فكرة المشروع؟

مختبر **Active Directory** تعليمي أصلي مبني على Docker ويعتمد على خادم **Samba Active Directory** واحد مع حاوية صغيرة تحتوي على أدوات الطالب. الهدف هو فهم بيئة الدومين، واكتشاف الـUsers والـGroups، ومراجعة خدمات LDAP وSMB، وتتبع أخطاء الصلاحيات وتسرب بيانات الحسابات.

يتضمن **4 مراحل عملية** مع Flags عشوائية تتجدد عند إنشاء لاب جديد، وتقييمًا آليًا من 100 نقطة، ونظام تلميحات تدريجيًا.

**ملاحظة تقنية:** المختبر يحاكي خدمات Active Directory من خلال Samba، ولا يشغّل Windows Server أو Windows Workstations. بعض الوظائف المتعلقة بنظام Windows ليست متاحة.

## المتطلبات

- Docker وDocker Compose v2.
- Python 3.9 أو أحدث.
- اتصال بالإنترنت عند إنشاء صور Docker أول مرة.
- يُفضّل توفير نحو 2 GB من الذاكرة الفارغة و3 GB من مساحة التخزين؛ هذه تقديرات إرشادية وليست نتائج قياس فعلي.

## التشغيل على Kali Linux

```bash
# بعد تنزيل ملفات المشروع من GitHub أو استخراج ZIP
cd green-armor-directory-range
python3 armorlab.py doctor
python3 armorlab.py up
python3 armorlab.py info
python3 armorlab.py shell
```

### بيانات الدخول الأولية

| العنصر | القيمة |
| --- | --- |
| Domain | `ARMOR.TEST` |
| Domain Controller | `dc` |
| Username | `student01` |
| Password | `GreenArmor2026!` |

من داخل حاوية الطالب:

```bash
dig @dc _ldap._tcp.armor.test SRV
smbclient -L //dc -U 'ARMOR\student01'
ldapsearch -x -H ldap://dc -D 'student01@armor.test' -W \
  -b 'DC=armor,DC=test' '(objectClass=user)' sAMAccountName description
```

## مراحل التاسك

| المرحلة | المطلوب | الدرجة |
| --- | --- | ---: |
| 01 | اكتشاف الخدمات والـShares | 15 |
| 02 | تعداد مستخدمي الدومين وخصائصهم عبر LDAP | 20 |
| 03 | إثبات وجود بيانات حساب خدمة متسربة | 25 |
| 04 | إثبات الوصول غير المصرح به إلى أرشيف حساس | 40 |
| **المجموع** | | **100** |

يُفضّل أن يسلّم الطالب تقريرًا مختصرًا يحتوي على الأدوات والأدلة والمخاطر والحلول، وليس Flags فقط.

## أوامر الإدارة

```bash
python3 armorlab.py submit 'GA{...}'
python3 armorlab.py score
python3 armorlab.py hint 02 1
python3 armorlab.py status
python3 armorlab.py logs
python3 armorlab.py down
python3 armorlab.py reset --yes
```

**تحذير:** أمر `reset --yes` يحذف بيانات المختبر ونتائج التحديات ويولّد Flags جديدة عند التشغيل التالي.

المختبر يحتوي على إعدادات ضعيفة متعمدة. شبكة Docker خاصة وغير متصلة بالشبكات الخارجية، ولا يتم فتح المنافذ على الجهاز المضيف. **لا تشغله داخل شبكة الجامعة أو شركة فعلية، ولا تُدخل بيانات دخول حقيقية.**

**الاعتماد:** JEHAD GHABEN — GREEN ARMOR ACADEMY  
[www.greenarmor.academy](https://www.greenarmor.academy)
