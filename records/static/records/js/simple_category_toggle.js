// Simple Category Form Toggle
(function () {
    'use strict';

    function init() {
        var $ = window.django ? window.django.jQuery : (window.jQuery || window.$);

        if (!$) {
            setTimeout(init, 100);
            return;
        }

        $(document).ready(function () {
            console.log('✓ Simple Category Toggle Loaded');

            function showCategoryFields() {
                var categoryField = $('#id_category');
                if (!categoryField.length) return;

                var categoryText = categoryField.find('option:selected').text().toLowerCase();
                console.log('Selected category:', categoryText);

                // Hide all category fieldsets first
                $('.namaz-fields').closest('fieldset').hide();
                $('.roza-fields').closest('fieldset').hide();
                $('.qurbani-fields').closest('fieldset').hide();

                // Show the relevant fieldset based on category
                if (categoryText.includes('namaz')) {
                    console.log('Showing Namaz fields');
                    var namazFieldset = $('.namaz-fields').closest('fieldset');
                    namazFieldset.show();
                    namazFieldset.removeClass('collapsed');
                } else if (categoryText.includes('roza')) {
                    console.log('Showing Roza fields');
                    var rozaFieldset = $('.roza-fields').closest('fieldset');
                    rozaFieldset.show();
                    rozaFieldset.removeClass('collapsed');
                } else if (categoryText.includes('qurbani')) {
                    console.log('Showing Qurbani fields');
                    var qurbaniFieldset = $('.qurbani-fields').closest('fieldset');
                    qurbaniFieldset.show();
                    qurbaniFieldset.removeClass('collapsed');
                }
            }

            // Trigger on category change
            $('body').on('change', '#id_category', function () {
                showCategoryFields();
            });

            // Trigger on select2 change (for autocomplete)
            $('body').on('select2:select', '#id_category', function () {
                showCategoryFields();
            });

            // Initial load
            setTimeout(showCategoryFields, 500);
            setTimeout(showCategoryFields, 1500);

            console.log('✓ Category toggle initialized');
        });
    }

    init();
})();
