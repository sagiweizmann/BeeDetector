<template>
  <!-- contact page -->
  <div>
    <h1>Contact</h1>
    <p>For any questions or concerns, please contact us at: <a href="mailto:" target="_top">
      </a></p>
  </div>

</template>

<script>
export default {
  layout: 'dashboard',
  middleware: ['redirect-if-not-authenticated'],
}
</script>
