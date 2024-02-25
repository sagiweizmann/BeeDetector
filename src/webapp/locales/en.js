export default {
  // All translations that you use in different places.
  common: {
    email: {
      label: 'Email',
      label_required: 'Email *',
      placeholder: 'Enter your email',
    },
    submit: 'Submit',
    retry: 'Retry',
    create: 'Create',
    update: 'Update',
    upload : 'Upload',
    analyze : 'Analyze the video',
    download_video : 'Download the video',
    download_csv : 'Download the csv',
    edit: 'Edit',
    delete: 'Delete',
    confirm: 'Confirm',
    cancel: 'Cancel',
    send_email: 'Send email',
    browse: 'Browse',
    reset: 'Reset',
    search: 'Search',
    export: 'Export',
    all: 'All',
    multiple_files: {
      placeholder: 'Choose files',
      drop_placeholder: 'Drop files',
    },
    single_file: {
      placeholder: 'Choose a file',
      drop_placeholder: 'Drop file',
    },
    user: {
      first_name: {
        label: 'First name',
        label_required: 'First name *',
        placeholder: 'Enter a first name',
      },
      last_name: {
        label: 'Last name',
        label_required: 'Last name *',
        placeholder: 'Enter a last name',
      },
      locale: {
        label: 'Locale',
        label_required: 'Locale *',
        select: 'Select a locale',
      },
      role: {
        label: 'Role',
        label_required: 'Role *',
        select: 'Select a role',
        administrator: 'Administrator',
        user: 'User',
      },
      profile_picture: 'Profile picture',
    },
    nav: {
      login: 'Login',
      register: 'Register',
      logout: 'Logout',
      my_profile: 'My profile',
      dashboard: 'Dashboard',
      welcome_dashboard: 'Welcome to the management dashboard',
      administration: 'Administration',
      users: 'Users',
    },
    list: {
      actions: 'Actions',
    },
  },
  bee_detector: {
    title: 'Welcome to The Bee Detector',
    description: 'Detect bees in the video',
    market_text: 'What do you want to bee today?',
    via_flying: 'Detect Via Flying video',
    via_box: 'Detect Via Box video',
    welcome_upload: 'Upload a video to detect bees',
    upload: 'Upload video',
  },
  // Translations of your components.
  components: {
    forms: {
      confirm_delete: {
        enter_confirm: 'Enter "Confirm"',
        danger_zone_message:
          'Warning, this section allows you to carry out dangerous and irremediable actions.',
      },
    },
  },
  // Translations of your layouts.
  layouts: {
    error: {
      generic_message: 'An error occurred',
      not_found_message: 'Page not found',
      access_forbidden_message: 'Access forbidden',
      home_page: 'Home page',
    },
  },
  // Translations of your mixins.
  mixins: {
    generic_toast: {
      success_message: 'Success 🎉',
    },
  },
  // Translations of your pages.
  pages: {
    home: {
      welcome: 'Welcome!',
      message: '',
    },
    login: {
      password: {
        label_required: 'Password *',
        placeholder: 'Enter your password',
      },
      error_message: 'The provided email or password is incorrect.',
      forgot_password: 'I forgot my password',
    },
    reset_password: {
      success_message:
        'If the address exists in our system, an email has been delivered with instructions to help you change your password.',
    },
    update_password: {
      new_password: {
        label_required: 'New password *',
        placeholder: 'Enter your new password',
      },
      password_confirmation: {
        label_required: 'Password confirmation *',
        placeholder: 'Enter again your new password',
      },
      invalid_token_message: 'Your token has either expired or is invalid.',
      success_message: 'Your password has been updated.',
    },
    register: {
      password: {
        label_required: 'Password *',
        placeholder: 'Enter your password',
      },
      password_repeat: {
        label_required: 'Repeat Password *',
        placeholder: 'Enter your password again',
      },
      error_message: 'The provided email or password is incorrect.',
      forgot_password: 'I forgot my password',
    },
  },
}
