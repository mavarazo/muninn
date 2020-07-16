(function ($) {
  'use strict'

  $(document).on('click', '[data-station-url]', function (event) {
    if ($('#audio-player')[0].paused === true) {
      $(this).addClass('active');

      $('#audio-player')
      $('#audio-player').attr('src', $(this).data('stationUrl'));
      $('#audio-player')[0].currentTime = 0;
      $('#audio-player')[0].play();
    } else {
      $(this).removeClass('active');
      $('#audio-player')[0].pause();
    }
  })

})(jQuery)