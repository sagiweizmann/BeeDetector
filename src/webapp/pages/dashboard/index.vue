<template>
  <div>
    <h1>{{ $t('common.nav.welcome_dashboard') }}</h1>
    <br/>
    <div class="d-flex flex-column align-items-center">
      <h1>{{ $t('bee_detector.description') }}</h1>
      <br/>
      <h3>{{ $t('bee_detector.market_text') }}</h3>
      <br/>
      <b-button variant="primary">
        {{ $t('bee_detector.via_flying') }}
      </b-button>
      <br/>
      <b-button variant="primary">
        {{ $t('bee_detector.via_box') }}
      </b-button>
    </div>
  </div>
</template>

<script>
export default {
  layout: 'dashboard',
  middleware: ['redirect-if-not-authenticated'],
}
</script>
