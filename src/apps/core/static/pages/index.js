$(document).ready(function () {
  const fullscreen = FullscreenImageView();

  const slider = SyncSlider({
    parentClass: '.gallery-slider',
    events: {
      imageClicked: function (event) {
        fullscreen.show(event.detail.src);
      },
    }
  });
});
