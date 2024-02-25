<template>
  <div>
    <h3>{{ $t('bee_detector.welcome_upload') }}</h3>
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
    <b-form v-if="videoShow" @submit.stop.prevent="onSubmitAnalyze">
      <video ref="videoPlayer" controls width="600" height="400">
        <source :src="videoSource" type="video/mp4">
        Your browser does not support the video tag.
      </video>
      <b-button
        type="submit"
        variant="primary"
        :disabled="videoSource === null"
      >
        {{ $t('common.analyze') }}
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
      videoResponse: null,
      videoSource: null,
      videoShow: false,
    }
  },
  methods: {
    async onSubmit() {
      this.resetFormErrors()
      this.displayGlobalOverlay()
      const formData = new FormData();
      formData.append('beeVideo', this.form.flying_video);
      formData.append('userId', this.user.id);
      //formData.append('userId', this.getUser().id);
      try {
        const response = await fetch(this.$config.apiURL + 'videos/upload', {
          method: 'POST',
          body: formData
        });

        if (!response.ok) {
          throw new Error('Failed to upload video');
        }

        console.log('Video uploaded successfully');
        this.form.flying_video = null;
        const responseData = await response.json();
        // store the response data
        this.videoResponse = responseData.target;
        this.videoShow = true;
        this.videoSource = this.$config.apiURL + this.videoResponse;

      } catch (e) {
        console.error(e);
        this.hydrateFormErrors(e)
      } finally {
        this.hideGlobalOverlay()
      }
    },
    async onSubmitAnalyze(){
      this.resetFormErrors()
      this.displayGlobalOverlay()
      const formData = new FormData();
      formData.append('videoPath', this.videoResponse);
      formData.append('userId', this.user.id);

      try {
        const response = await fetch(this.$config.apiURL + 'videos/analyze', {
          method: 'POST',
          body: formData
        });

        if (!response.ok) {
          throw new Error('Failed to analyze video');
        }
        const responseData = await response.json();
        // store the response data
        //this.videoResponse = responseData.target;
        //console.log(this.videoResponse);
        console.log('Video analyzed successfully');

      } catch (e) {
        console.error(e);
        this.hydrateFormErrors(e)
      } finally {
        this.hideGlobalOverlay()
      }
    }
  },
}
</script>

<style scoped>

</style>
