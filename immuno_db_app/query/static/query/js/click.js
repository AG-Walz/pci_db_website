document.addEventListener('DOMContentLoaded', function() {
    // boxes to links
    var idLinkMap = {
        'skin_box_overlay': '/psms/?biological_material=SKIN&dignity=benign',
        'skin_box_malignant_overlay': '/psms/?biological_material=SKIN&dignity=malignant',
        'thyroid_box_overlay': '/psms/?biological_material=THYROID_GLAND&dignity=benign',
        'thyroid_box_malignant_overlay': '/psms/?biological_material=THYROID_GLAND&dignity=malignant',
        'ovaries_box_overlay': '/psms/?biological_material=OVARY&dignity=benign',
        'ovaries_box_malignant_overlay': '/psms/?biological_material=OVARY&dignity=malignant',
        'bladder_box_overlay': '/psms/?biological_material=URINARY_BLADDER&dignity=benign',
        'bladder_box_malignant_overlay': '/psms/?biological_material=URINARY_BLADDER&dignity=malignant',
        'blood_plasma_box_overlay': '/psms/?biological_material=BLOOD_PLASMA&dignity=benign',
        'blood_plasma_box_malignant_overlay': '/psms/?biological_material=BLOOD_PLASMA&dignity=malignant',
        'colon_box_overlay': '/psms/?biological_material=COLON&dignity=benign',
        'colon_box_malignant_overlay': '/psms/?biological_material=COLON&dignity=malignant',
        'stomach_box_overlay': '/psms/?biological_material=STOMACH&dignity=benign',
        'stomach_box_malignant_overlay': '/psms/?biological_material=STOMACH&modifications=&dignity=malignant',
        'esophagus_box_overlay': '/psms/?biological_material=ESOPHAGUS&dignity=benign',
        'esophagus_box_malignant_overlay': '/psms/?biological_material=ESOPHAGUS&dignity=malignant',
        'testes_box_overlay': '/psms/?biological_material=TESTIS&modifications=&dignity=benign',
        'testes_box_malignant_overlay': '/psms/?biological_material=TESTIS&modifications=&dignity=malignant',
        'small_intestine_box_overlay': '/psms/?biological_material=SMALL_INTESTINE&modifications=&dignity=benign',
        'small_intestine_box_malignant_overlay': '/psms/?biological_material=SMALL_INTESTINE&modifications=&dignity=malignant',
        'kidneys_box_overlay': '/psms/?biological_material=KIDNEY&modifications=&dignity=benign',
        'kidneys_box_malignant_overlay': '/psms/?biological_material=KIDNEY&modifications=&dignity=malignant',
        'adrenal_gland_box_overlay': '/psms/?biological_material=ADRENAL_GLAND&modifications=&dignity=benign',
        'adrenal_gland_box_malignant_overlay': '/psms/?biological_material=ADRENAL_GLAND&modifications=&dignity=malignant',
        'liver_box_overlay': '/psms/?biological_material=LIVER&modifications=&dignity=benign',
        'liver_box_malignant_overlay': '/psms/?biological_material=LIVER&modifications=&dignity=malignant',
        'lung_box_overlay': '/psms/?biological_material=LUNG&modifications=&dignity=benign',
        'lung_box_malignant_overlay': '/psms/?biological_material=LUNG&modifications=&dignity=malignant',
        'thymus_box_overlay': '/psms/?biological_material=THYMUS&modifications=&dignity=benign',
        'thymus_box_malignant_overlay': '/psms/?biological_material=THYMUS&modifications=&dignity=malignant',
        'pbmc_box_overlay': '/psms/?biological_material=PBMC&modifications=&dignity=benign',
        'pbmc_box_malignant_overlay': '/psms/?biological_material=PBMC&modifications=&dignity=malignant',
        'cerebrum_box_overlay': '/psms/?biological_material=BRAIN&modifications=&dignity=benign',
        'cerebrum_box_malignant_overlay': '/psms/?biological_material=BRAIN&modifications=&dignity=malignant',
        'head_and_neck_box_overlay': '/psms/?biological_material=HEAD_AND_NECK&modifications=&dignity=benign',
        'head_and_neck_box_malignant_overlay': '/psms/?biological_material=HEAD_AND_NECK&modifications=&dignity=malignant',
        'pancreas_box_overlay': '/psms/?biological_material=PANCREAS&modifications=&dignity=benign',
        'pancreas_box_malignant_overlay': '/psms/?biological_material=PANCREAS&modifications=&dignity=malignant',
        'cerebellum_box_overlay': '/psms/?biological_material=CEREBELLUM&modifications=&dignity=benign',
        'aorta_box_overlay': '/psms/?biological_material=AORTA&modifications=&dignity=benign',
        'heart_box_overlay': '/psms/?biological_material=HEART&modifications=&dignity=benign',
        'spleen_box_overlay': '/psms/?biological_material=SPLEEN&modifications=&dignity=benign'
    };


    // Add click event, pointer cursor, and hover effect to each ID in the idLinkMap
    Object.keys(idLinkMap).forEach(function(id) {
        var url = idLinkMap[id];
        var element = document.getElementById(id);

        // Set pointer to cursor to indicate clickability
        element.style.cursor = 'pointer';

        // save the original fill and opacity styles
        var originalFill = element.style.fill || window.getComputedStyle(element).fill;
        var originalOpacity = element.style.fillOpacity || window.getComputedStyle(element).fillOpacity;

        // link to psms site on click on box
        element.addEventListener('click', function() {
            console.log('Moving to:', url);
            window.location.href = url;
        });

        // highlight on hover
        element.addEventListener('mouseover', function() {
            // hover effect when cursor is over clickable area
            element.style.fillOpacity = '0.5'; // reduce opacity
            element.style.fill = '#ff4d2e';
        });

        element.addEventListener('mouseout', function() {
            // Reset hover effect (to previous color and opacity)
            element.style.fillOpacity = originalOpacity; 
            element.style.fill = originalFill;
        });
    });
});
