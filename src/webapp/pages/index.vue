<template>
  <div>
      <h1 class="display-2">
        {{ $t('pages.home.welcome') }}
        <small class="text-muted">Bee Detector</small>
      </h1>
      <p class="lead" v-if="!isAuthenticated">
        {{ $t('pages.home.message') }}
      </p>
    <!-- btns of register and login  if not authenticated -->
    <!-- text of welcome and description  if not authenticated -->
    <b-row>
      <b-col cols="auto">
        <b-button
          v-if="!isAuthenticated"
          :to="localePath({ name: 'login' })"
          variant="primary"
        >
          {{ $t('common.nav.login') }}
        </b-button>
      </b-col>
      <b-col cols="auto">
        <b-button
          v-if="!isAuthenticated"
          :to="localePath({ name: 'register' })"
          variant="primary"
        >
          {{ $t('common.nav.register') }}
        </b-button>
      </b-col>
    </b-row>
    <!-- gif of walking bee -->
    <div class="d-flex justify-content-center">
      <b-img
        :src="walkGifurl"
        alt="Walking Bee"
        class="img-fluid"
      ></b-img>
    </div>
  </div>
</template>
<script>
import { Auth } from '@/mixins/auth'
import walkgif from "@/assets/images/WalkingBeeDemo.gif";

export default {
  mixins: [Auth],
  data() {
    return {
      walkGifurl : walkgif,
    }
  },
}
</script>
