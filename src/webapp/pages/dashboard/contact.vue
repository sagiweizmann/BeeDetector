<template>
  <!-- contact page -->
  <div>
    <h1>{{ $t('bee_detector.contact') }}</h1>
    <p>{{ $t('bee_detector.contact_text') }}
      <br>
      <a href="mailto:hadasda1@ac.sce.ac.il" target="_top">{{ $t('bee_detector.contact_name_hadas') }}
      </a>
      <br>
      <a href="mailto:tammarm@gmail.com" target="_top">{{ $t('bee_detector.contact_name_tamar') }}
      </a>
    </p>
  </div>

</template>

<script>
export default {
  layout: 'dashboard',
  middleware: ['redirect-if-not-authenticated'],
}
</script>
