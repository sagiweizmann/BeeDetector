<template>
<!-- faq page -->
  <div>
    <h1>FAQ</h1>
    <p>Q: What is the purpose of this application?</p>
    <p>A: The purpose of this application is to analyze videos of bees and extract data from them.</p>
    <p>Q: What kind of data can be extracted from the videos?</p>
    <p>A: The application can extract the following data from the videos: the number of bees, the distance traveled by the bees, and the time spent by the bees in the video.</p>
    <p>Q: What kind of videos can be analyzed?</p>
    <p>A: The application can analyze videos of bees that are in the .mp4 format.</p>
    <p>Q: What is the minimum and maximum distance that the bees can travel?</p>
    <p>A: The minimum and maximum distance that the bees can travel is 0 and 1000, respectively.</p>
    <p>Q: What is the minimum and maximum time that the bees can spend in the video?</p>
    <p>A: The minimum and maximum time that the bees can spend in the video is 0 and 1000, respectively.</p>
    <p>Q: What is the minimum and maximum number of bees that can be in the video?</p>
    <p>A: The minimum and maximum number of bees that can be in the video is 0 and 1000, respectively.</p>
  </div>

</template>

<script>
export default {
  layout: 'dashboard',
  middleware: ['redirect-if-not-authenticated'],
}
</script>
