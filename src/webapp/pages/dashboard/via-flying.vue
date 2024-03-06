<template>
  <div>
    <b-form @submit.stop.prevent="onSubmit">
      <h3>{{ $t('bee_detector.welcome_upload') }}</h3>
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
      <video ref="videoPlayer" controls width="200" height="150">
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
    <br/>
    <div v-if="analyzedVideoShow" id="analyzed-video">
      <video ref="analyzedVideoPlayer" controls width="250" height="150">
        <source :src="analyzedVideoSource">
        Your browser does not support the video tag.
      </video>
      <div id="analyzed-video-buttons">
        <a :href="analyzedVideoSource" :download="analyzedName">
          <b-button
            variant="primary"
          >
            {{ $t('common.download_video') }}
          </b-button>
        </a>
        <a :href="analyzedCsvFile" download>
          <b-button
            variant="primary"
          >
            {{ $t('common.download_csv') }}
          </b-button>
        </a>
      </div>
    </div>
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
      analyzedVideoSource: null,
      downloadVideoSource: null,
      analyzedVideoShow: false,
      analyzedCsvFile: null,
      analyzedName: null,
    }
  },
  methods: {
    async onSubmit() {
      this.resetFormErrors()
      this.displayGlobalOverlay()
      this.videoShow = false;
      this.analyzedVideoShow = false;
      this.analyzedName = this.form.flying_video;
      const formData = new FormData();
      formData.append('beeVideo', this.form.flying_video);
      formData.append('userId', this.user.id);
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
        const response = await fetch(this.$config.apiURL + 'videos/analyzeflying', {
          method: 'POST',
          body: formData
        });

        if (!response.ok) {
          throw new Error('Failed to analyze video');
        }
        const responseData = await response.json();

        this.analyzedVideoShow = true;
        this.analyzedVideoSource = this.$config.apiURL + responseData.videoOutput;
        this.downloadVideoSource = await this.download(responseData.videoOutput);
        this.analyzedCsvFile = this.$config.apiURL + responseData.csvOutput;
        this.analyzedName = this.analyzedName.name.replace('.mp4', '_analyzed.mp4');

        console.log('Video analyzed successfully');

      } catch (e) {
        console.error(e);
        this.hydrateFormErrors(e)
      } finally {
        this.hideGlobalOverlay()
      }
    },
    download(filename) {
      const downloadData = new FormData();
      downloadData.append('filename', filename);
      return fetch(this.$config.apiURL + 'videos/download', {
        method: 'POST',
        body: downloadData
      }).then(response => response.blob())
        .then(blob => {
          return URL.createObjectURL(blob);
        });
    },
  },
}
</script>

<style scoped>

form {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px
}

#analyzed-video {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

#analyzed-video-buttons {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 10px;
}

</style>
