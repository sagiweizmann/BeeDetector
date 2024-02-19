<template>
  <div>
    <b-row>
      <h3>
        {{ $t('bee_detector.welcome_upload') }}
      </h3>
    </b-row>
    <b-form @submit.stop.prevent="onSubmit">
      <b-form-group
        id="input-group-video"
        :label="$t('bee_detector.upload')"
        label-for="input-video"
      >
        <b-form-file
          id="input-video"
          v-model="form.flying_video"
          :placeholder="$t('common.single_file.placeholder')"
          :drop-placeholder="$t('common.single_file.drop_placeholder')"
          :browse-text="$t('common.browse')"
          :state="formState('flying_video')"
        ></b-form-file>
        <div v-if="form.flying_video !== null" class="mt-3">
          <FilesList :files="[form.flying_video]" />
        </div>
        <b-form-invalid-feedback :state="formState('flying_video')">
          <ErrorsList :errors="formErrors('flying_video')" />
        </b-form-invalid-feedback>
      </b-form-group>
      <b-button
        type="submit"
        variant="primary"
        :disabled="form.flying_video === null"
      >
        {{ $t('common.upload') }}
      </b-button>
    </b-form>
  </div>
</template>

<script>
import FilesList from "@/components/forms/FilesList.vue";
import ErrorsList from "@/components/forms/ErrorsList.vue";
import {Form} from "@/mixins/form";
import {Auth} from "@/mixins/auth";
import {Roles} from "@/mixins/roles";
import {Images} from "@/mixins/images";
import {GlobalOverlay} from "@/mixins/global-overlay";
import {UpdateProfilePictureMutation} from "@/graphql/users/update_profile_picture.mutation";

export default {
  components: {FilesList, ErrorsList},
  mixins: [Form, Auth, Roles, Images, GlobalOverlay],
  layout: 'dashboard',
  middleware: ['redirect-if-not-authenticated'],
  data() {
    return {
      form: {
        flying_video: null,
      },
    }
  },
  methods: {
    async onSubmit() {
      this.resetFormErrors()
      this.displayGlobalOverlay()

      // try {
      //   const result = await this.$graphql.request(
      //     UpdateProfilePictureMutation,
      //     {
      //       flying_video: this.form.flying_video,
      //     }
      //   )
      //
      //   this.setUserProfilePicture(result.updateProfilePicture.profilePicture)
      //   this.form.flying_video = null
      // } catch (e) {
      //   this.hydrateFormErrors(e)
      // } finally {
      //   this.hideGlobalOverlay()
      // }
    },
  },
}
</script>

<style scoped>

</style>
