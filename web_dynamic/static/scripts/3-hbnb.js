$(document).ready(function() {
    const amenities = {};
    $('.container').on('change', 'input[type="checkbox"]', function() {
      if (this.checked) {
        amenities[$(this).data('id')] = $(this).data('name');
      } else {
        delete amenities[$(this).data('id')];
      }
      $('.amenities h4').text(Object.values(amenities).join(', '));
    });
  });
  