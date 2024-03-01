export default {
  common: {
    email: {
      label: 'אימייל',
      label_required: 'אימייל *',
      placeholder: 'הזינו את כתובת האימייל שלכם',
    },
    submit: 'שלח',
    retry: 'נסה שוב',
    create: 'צור',
    update: 'עדכן',
    upload : 'העלה',
    analyze : 'נתח את הוידאו',
    download_video : 'הורד את הוידאו',
    download_csv : 'הורד קובץ CSV',
    edit: 'ערוך',
    delete: 'מחק',
    confirm: 'אשר',
    cancel: 'ביטול',
    send_email: 'שלח אימייל',
    browse: 'עיין',
    reset: 'אתחל',
    search: 'חיפוש',
    export: 'יצוא',
    all: 'הכל',
    multiple_files: {
      placeholder: 'בחרו קבצים',
      drop_placeholder: 'שחררו קבצים',
    },
    single_file: {
      placeholder: 'בחרו קובץ',
      drop_placeholder: 'שחררו קובץ',
    },
    user: {
      first_name: {
        label: 'שם פרטי',
        label_required: 'שם פרטי *',
        placeholder: 'הזינו שם פרטי',
      },
      last_name: {
        label: 'שם משפחה',
        label_required: 'שם משפחה *',
        placeholder: 'הזינו שם משפחה',
      },
      locale: {
        label: 'אזור',
        label_required: 'אזור *',
        select: 'בחרו אזור',
      },
      role: {
        label: 'תפקיד',
        label_required: 'תפקיד *',
        select: 'בחרו תפקיד',
        administrator: 'מנהל',
        user: 'משתמש',
      },
      profile_picture: 'תמונת פרופיל',
    },
    nav: {
      login: 'התחברות',
      register: 'הרשמה',
      logout: 'התנתקות',
      my_profile: 'הפרופיל שלי',
      dashboard: 'לוח בקרה',
      welcome_dashboard: 'ברוכים הבאים ללוח הבקרה לניהול',
      administration: 'ניהול',
      users: 'משתמשים',
    },
    list: {
      actions: 'פעולות',
    },
  },
  bee_detector: {
    title: 'ברוכים הבאים למגלה הדבורים',
    description: 'זיהוי דבורים בוידאו',
    market_text: 'מה תרצו לזהות היום?',
    via_flying: 'זיהוי דבורה מעופפת',
    via_box: 'זיהוי דבורה בכוורת',
    download_package : 'הורד חבילת קוד',
    link_collab : 'קישור לקולאב של Google',
    faq : 'שאלות נפוצות',
    contact: 'יצירת קשר',
    welcome_upload: 'העלו וידאו לזיהוי דבורים',
    upload: 'העלה וידאו',
    max_fps : 'מספר תמונות לשנייה',
    min_move_distance : 'מרחק מינימלי לתנועה',
    max_move_distance : 'מרחק מקסימלי לתנועה',
  },
  components: {
    forms: {
      confirm_delete: {
        enter_confirm: 'הזינו "אישור"',
        danger_zone_message: 'אזור מסוכן! פעולות בלתי הפיכות עשויות להתרחש כאן.',
      },
    },
  },
  layouts: {
    error: {
      generic_message: 'אירעה שגיאה',
      not_found_message: 'העמוד לא נמצא',
      access_forbidden_message: 'גישה נדחתה',
      home_page: 'דף הבית',
    },
  },
  mixins: {
    generic_toast: {
      success_message: 'הצלחה 🎉',
    },
  },
  pages: {
    home: {
      welcome: 'ברוכים הבאים!',
      message: '',
    },
    login: {
      password: {
        label_required: 'סיסמה *',
        placeholder: 'הזינו את הסיסמה שלכם',
      },
      error_message: 'כתובת האימייל או הסיסמה שסופקו אינם נכונים.',
      forgot_password: 'שכחתי את הסיסמה שלי',
    },
    reset_password: {
      success_message: 'אם הכתובת קיימת במערכת שלנו, אז אימייל עם הוראות לשינוי הסיסמה נשלח אליך.',
    },
    update_password: {
      new_password: {
        label_required: 'סיסמה חדשה *',
        placeholder: 'הזינו את הסיסמה החדשה שלכם',
      },
      password_confirmation: {
        label_required: 'אימות סיסמה *',
        placeholder: 'הזינו שוב את הסיסמה החדשה שלכם',
      },
      invalid_token_message: 'האסימון שלך פג או שאינו תקין.',
      success_message: 'הסיסמה שלך עודכנה בהצלחה.',
    },
    register: {
      password: {
        label_required: 'סיסמה *',
        placeholder: 'הזינו את הסיסמה שלכם',
      },
      password_repeat: {
        label_required: 'אימות סיסמה *',
        placeholder: 'הזינו שוב את הסיסמה שלכם',
      },
      error_message: 'כתובת האימייל או הסיסמה שסופקו אינם נכונים.',
      forgot_password: 'שכחתי את הסיסמה שלי',
    },
  },
}
