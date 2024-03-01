import logo from '@/assets/images/logo_small.png'
import defaultProfilePicture from '@/assets/images/default-profile-picture.svg'
import defaultProfilePictureWhite from '@/assets/images/default-profile-picture-white.svg'
import sceLogo from '@/assets/images/samilogo.png'
import argiLogo from '@/assets/images/argilogo.png'

export const Images = {
  data() {
    return {
      logoImageURL: logo,
      sceLogoImageURL: sceLogo,
      argiLogoImageURL: argiLogo,
      defaultProfilePictureURL: defaultProfilePicture,
      defaultProfilePictureWhiteURL: defaultProfilePictureWhite,
    }
  },
  methods: {
    userProfilePictureURL(filename) {
      return this.$config.apiURL + 'users/profile-picture/' + filename
    },
  },
}
