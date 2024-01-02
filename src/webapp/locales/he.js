export default {
  // כל התרגומים שאתה משתמש במקומות שונים.
  common: {
    email: {
      label: 'דוא"ל',
      label_required: 'דוא"ל *',
      placeholder: 'הזן את כתובת הדוא"ל שלך',
    },
    submit: 'שלח',
    retry: 'נסה שוב',
    create: 'צור',
    update: 'עדכן',
    edit: 'ערוך',
    delete: 'מחק',
    confirm: 'אשר',
    cancel: 'בטל',
    send_email: 'שלח דוא"ל',
    browse: 'עיין',
    reset: 'אפס',
    search: 'חפש',
    export: 'יצא',
    all: 'הכל',
    multiple_files: {
      placeholder: 'בחר קבצים',
      drop_placeholder: 'זרוק קבצים',
    },
    single_file: {
      placeholder: 'בחר קובץ',
      drop_placeholder: 'זרוק קובץ',
    },
    user: {
      first_name: {
        label: 'שם פרטי',
        label_required: 'שם פרטי *',
        placeholder: 'הזן שם פרטי',
      },
      last_name: {
        label: 'שם משפחה',
        label_required: 'שם משפחה *',
        placeholder: 'הזן שם משפחה',
      },
      locale: {
        label: 'אזור',
        label_required: 'אזור *',
        select: 'בחר אזור',
      },
      role: {
        label: 'תפקיד',
        label_required: 'תפקיד *',
        select: 'בחר תפקיד',
        administrator: 'מנהל',
        user: 'משתמש',
      },
      profile_picture: 'תמונת פרופיל',
    },
    nav: {
      login: 'התחברות',
      logout: 'התנתקות',
      my_profile: 'הפרופיל שלי',
      dashboard: 'לוח בקרה',
      administration: 'ניהול',
      users: 'משתמשים',
    },
    list: {
      actions: 'פעולות',
    },
  },
  // תרגומים של הרכיבים שלך.
  components: {
    forms: {
      confirm_delete: {
        enter_confirm: 'הזן "אשר"',
        danger_zone_message:
          'אזהרה, סעיף זה מאפשר לך לבצע פעולות מסוכנות ובלתי הפיכות.',
      },
    },
  },
  // תרגומים של התצורות שלך.
  layouts: {
    error: {
      generic_message: 'אירעה שגיאה',
      not_found_message: 'דף לא נמצא',
      access_forbidden_message: 'גישה אסורה',
      home_page: 'דף הבית',
    },
  },
  // תרגומים של הבלנדים שלך.
  mixins: {
    generic_toast: {
      success_message: 'הצלחה 🎉',
    },
  },
  // תרגומים של הדפים שלך.
  pages: {
    home: {
      welcome: 'ברוך הבא!',
      message:
        'קוד המקור של Symfony מספק יישום מדומה עם מושגים יסודיים ותכליתיים לעזור לך לבנות אפליקציה ווב מודרנית.',
    },
    login: {
      password: {
        label_required: 'סיסמה *',
        placeholder: 'הזן את הסיסמה שלך',
      },
      error_message: 'הדוא"ל או הסיסמה שסופקו אינם נכונים.',
      forgot_password: 'שכחתי את הסיסמה שלי',
    },
    reset_password: {
      success_message:
        'אם הכתובת קיימת במערכת שלנו, נשלח אליך דוא"ל עם הוראות לעזרה בשינוי הסיסמה שלך.',
    },
    update_password: {
      new_password: {
        label_required: 'סיסמה חדשה *',
        placeholder: 'הזן את הסיסמה החדשה שלך',
      },
      password_confirmation: {
        label_required: 'אימות סיסמה *',
        placeholder: 'הזן שוב את הסיסמה החדשה שלך',
      },
      invalid_token_message: 'הטוקן שלך פג או אינו תקף.',
      success_message: 'הסיסמה שלך עודכנה בהצלחה.',
    },
  },
}
