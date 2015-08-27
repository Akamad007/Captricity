
jQuery(document).ready(function() {
	
	/*
	    Wow
	*/
	new WOW().init();
	
	
	/*
	    Image popup (home latest work)
	*/
	$('.view-work').magnificPopup({
		type: 'image',
		gallery: {
			enabled: true,
			navigateByImgClick: true,
			preload: [0,1] // Will preload 0 - before current, and 1 after the current image
		},
		image: {
			tError: 'The image could not be loaded.',
			titleSrc: function(item) {
				return item.el.parent('.work-bottom').siblings('img').attr('alt');
			}
		},
		callbacks: {
			elementParse: function(item) {
				item.src = item.el.attr('href');
			}
		}
	});
	
});
    
    
	
	
    
    

jQuery(window).load(function() {
	
	
	// image popup	
	$('.portfolio-box h3').magnificPopup({
		type: 'image',
		gallery: {
			enabled: true,
			navigateByImgClick: true,
			preload: [0,1] // Will preload 0 - before current, and 1 after the current image
		},
		image: {
			tError: 'The image could not be loaded.',
			titleSrc: function(item) {
				return item.el.text();
			}
		},
		callbacks: {
			elementParse: function(item) {
				var box_container = item.el.parents('.portfolio-box-container');
				if(box_container.hasClass('portfolio-video')) {
					item.type = 'iframe';
					item.src = box_container.data('portfolio-big');
				}
				else {
					item.type = 'image';
					item.src = box_container.find('img').attr('src');
				}
			}
		}
	});
	
	
});
