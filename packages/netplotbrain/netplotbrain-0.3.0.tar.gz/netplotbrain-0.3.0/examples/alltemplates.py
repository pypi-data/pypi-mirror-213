import templateflow.api as tf
import netplotbrain 
import json 
import matplotlib.pyplot as plt

with open ('./netplotbrain/templatesettings/template_get_kwargs.json', 'r') as f:
    kwargs = json.load(f)
# Get all templates
templates = tf.templates()
template_paths = []
template_names = []
cohort = {'MNIInfant': 11,
          'MNIPediatricAsym': 5,
          'RESILIENT': 4,
          'UNCInfant': 3}
style = 'surface'
for template in templates[4:]:
    if template == 'fsLR':
        #ignore as it is not compatible at the moment (no nii)
        pass
    else:
        print(template)
        #try:
        if template in cohort:
            for c in range(cohort[template]):
                netplotbrain.plot(template=template + '_cohort-' + str(c+1), 
                            view=['SLR'],
                            template_style=style,
                            savename='./examples/templateflow_templates/' + style + '/template_' + template + '_cohort-' + str(c+1) + '.png', 
                            subtitles=template)
                plt.close('all')

        else:
            netplotbrain.plot(template=template, 
                            view=['SLR'],
                            template_style=style,
                            savename='./examples/templateflow_templates/' + style + '/template-' + template + '.png', 
                            subtitles=template)
            plt.close('all')
        #except:
        #    print('---error---')
        #    fails.append(t)