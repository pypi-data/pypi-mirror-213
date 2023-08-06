import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches


def make_greedy_plot(factual_score, features_data, class_names, save_path):
    fig = plt.figure(figsize=(7, 1 * len(features_data))) # noqa

    scatter_points = [f['score'] for f in features_data]
    scatter_points.insert(0, factual_score)

    plt.plot(scatter_points, range(len(scatter_points)),
             color='#c4c4c4', linestyle='dashed', zorder=0)
    for c_idx, point in enumerate(scatter_points):
        plt.scatter(
            [point],
            [c_idx],
            color='#ff0055D2' if point < 0.5 else '#008ae7D2',
            s=100)

    features_names = ['Factual']
    for feat_idx, f in enumerate(features_data):
        features_names.append(
            f'{f["name"]} ({f["factual"]}➜{f["counterfactual"]})')
    max_feat_names_length = max([len(feat_name)
                                for feat_name in features_names])

    # Plot a vertical line at the threshold score
    plt.axvline(x=0.5, color='#c20000', zorder=0, linewidth=0.5)

    # Plot a vertical line at the factual score
    plt.axvline(x=factual_score, color='#ff0055D2',
                linestyle='dashed', zorder=0)
    plt.text(factual_score - 0.088, len(features_names)*1.04 -
             0.9, 'Factual Score', color='#ff0055D2')

    # Plot a vertical line at the counterfactual score
    plt.axvline(x=scatter_points[-1],
                color='#008ae7D2', linestyle='dashed', zorder=0)
    plt.text(scatter_points[-1] - 0.15, len(features_names)*1.04 -
             0.9, 'Counterfactual Score', color='#008ae7D2')

    for feat_idx, feat_name in enumerate(features_names):
        plt.text(-0.02 * max_feat_names_length, feat_idx,
                 feat_name, color='#545454', fontsize=12)

    # Print binary class
    class_0_name = list(class_names.values())[0]
    class_1_name = list(class_names.values())[1]
    size_factual_class = mpl.textpath.TextPath(
        (0, 0), class_0_name).get_extents().width * 0.003
    plt.text(0.47 - size_factual_class - max([len(f) for f in features_names])*0.0001, len(features_names)
             - 0.75 + (len(features_names) + 1)*0.04,
             class_0_name, color='#ff0055D2', fontweight='bold')
    plt.text(0.49, len(features_names) - 0.75 + (len(features_names) + 1)*0.04, '➜',
             color='#c20000', fontweight='bold')
    plt.text(0.52, len(features_names) - 0.75 + (len(features_names) + 1)
             * 0.04, class_1_name, color='#008ae7D2', fontweight='bold')

    plt.gca().axes.get_yaxis().set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    # Set limit of x axis from 0 to 1
    plt.xlim(-0.05, 1)

    if save_path:
        plt.savefig(save_path, bbox_inches='tight')


def make_countershapley_plot(factual_score, features_data, classes, save_path):
    fig = plt.figure(figsize=(10, 1.5))
    ax = fig.add_subplot(111)
    scale_x = 100
    scale_y = 100
    bar_y_height = scale_y / 2
    bar_y_height_sub = scale_y / 8.0
    fontsize = 10
    color_bar = '#48C975D2'
    cf_score = features_data[-1]['score']
    sum_countershapley = cf_score - factual_score

    # Beak must be always the 4%
    def create_bar(start_x, end_x, no_beak=False):

        verts = [
            (start_x, 0.),  # left, bottom
            (start_x, bar_y_height),  # left, top
            (end_x - 4, bar_y_height),  # right, top
            (end_x, bar_y_height),  # right, top
            (end_x, 0.),  # right, bottom
            (0., 0.),  # ignored
        ]

        codes = [
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO if no_beak else Path.CURVE3,
            Path.LINETO,
            Path.CLOSEPOLY,
        ]

        return Path(verts, codes)

    prev_score = factual_score
    current_x = 0
    x_left_pos = []
    for _, feat_data in enumerate(features_data):
        x_left_pos.append(current_x)
        x_size = feat_data['x'] * 100 / scale_x + current_x

        # Plot text for feature name
        plt.text(
            current_x + (x_size - current_x) / 2 -
            len(feat_data['name']) * fontsize / 10 / 2,
            -40,
            feat_data['name'],
            color='#545454',
            fontsize=fontsize)

        feature_change_text = f"{feat_data['factual']}➜{feat_data['counterfactual']}"

        # Plot bar up to 50% of the plot with the factual color
        ax.add_patch(patches.PathPatch(create_bar(
            current_x, x_size), facecolor=color_bar, lw=0))

        # Plot text for feature changes
        feat_change_text = mpl.textpath.TextPath(
            (0, 0), feature_change_text, size=fontsize)
        plt.text(
            current_x + (x_size - current_x)/2 -
            feat_change_text.get_extents().width * 0.1,
            -80,
            feature_change_text,
            color='#545454',
            fontsize=fontsize)

        feat_cs_score_percentage = round(
            (feat_data['score'] - prev_score)/sum_countershapley*100, 1)
        feat_cs_score_percentage_text = mpl.textpath.TextPath(
            (0, 0), f'{feat_cs_score_percentage}%', size=fontsize)
        plt.text(
            current_x + (x_size - current_x) / 2 -
            feat_cs_score_percentage_text.get_extents().width * 0.085,
            bar_y_height_sub,
            f'{feat_cs_score_percentage}%',
            color='white',
            fontsize=fontsize,
            weight="bold")

        current_x = x_size
        prev_score = feat_data['score']

    # Print CF score
    plt.text(
        current_x,
        scale_y,
        round(features_data[-1]['score'], 2),
        color='#008ae7',
        fontsize=fontsize)

    # Draw bar for the factual score
    plt.bar(0, scale_y - 10, width=0.5, color='#ff0055', linewidth=1)
    plt.text(-5, scale_y + fontsize * 4, 'Factual Score',
             color='#ff0055', fontsize=fontsize)
    plt.text(0, scale_y, factual_score, color='#ff0055',
             fontsize=fontsize)

    # Plot bar for the counterfactual score
    plt.bar(current_x, scale_y - 10, width=0.5, color='#008ae7', linewidth=1)
    plt.text(current_x - 10, scale_y + fontsize * 4,
             'Counterfactual Score', color='#008ae7', fontsize=fontsize)

    # Remove y axis
    plt.gca().axes.get_yaxis().set_visible(False)
    plt.gca().axes.get_xaxis().set_visible(False)
    # Remove square around the plot
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)

    for l_pos in x_left_pos:  # little dividers between x labels
        plt.bar(l_pos, -scale_y + 10, width=0.2, color='#cccccc', linewidth=0)
    plt.bar(scale_x, -scale_y + 10, width=0.2,
            color='#cccccc', linewidth=0)  # divider at the end

    ax.set_xlim(0, scale_x)
    ax.set_ylim(-scale_y, scale_y + 70)

    if save_path is not None:
        plt.savefig(save_path, bbox_inches='tight')

    plt.show()


def make_constellation_plot(factual_score, single_points_chart, text_features, mulitple_points_chart,
                            mulitple_points_chart_y, single_points, class_names, cf_score, point_to_pred, save_path):
    x_dim = 10
    y_dim = 4
    y_lim_low = -0.1
    y_lim_high = len(single_points_chart) - 0.9
    x_lim_low = 0
    x_lim_high = 1

    fig = plt.figure(figsize=(x_dim, y_dim))
    ax = fig.add_subplot(111)

    ax.set_xlim(x_lim_low, x_lim_high)
    ax.set_ylim(y_lim_low, y_lim_high)

    # Plot single change points
    for idx_p, p in enumerate(single_points_chart):
        plt.scatter([p[1]], [p[0]], color='#008ae7D2' if p[1]
                    >= 0.5 else '#ff0055D2', s=100)

    # Plot feature names and value changes
    max_text_features = max([len(f) for f in text_features])
    for i in range(len(text_features)):
        plt.text(-0.012*max_text_features, i,
                 text_features[i], color='#545454', fontsize=12)

    # Verify if there are multiple change points
    if len(mulitple_points_chart) > 0:
        # Plot multiple change points
        plt.scatter(mulitple_points_chart[:, 1],
                    mulitple_points_chart_y,
                    color=['#E0423A' if s <
                           0.5 else 'blue' for s in mulitple_points_chart[:, 1]],
                    s=10)

    # Plot counterfactual point
    cf_pred_x_1 = np.mean([*range(len(single_points))])
    plt.scatter([cf_score], [cf_pred_x_1], color='#008ae7D2' if cf_score
                >= 0.5 else '#ff0055D2', s=100)

    # Plot a vertical line at the threshold
    plt.axvline(x=0.5, color='#c20000', zorder=0, linewidth=0.5)

    # Plot a vertical line at the factual score
    plt.axvline(x=factual_score, color='#ff0055D2',
                linestyle='dashed', zorder=0)
    plt.text(factual_score - 0.06, len(text_features) *
             1.01 - 0.9, 'Factual Score', color='#ff0055D2')

    # Plot a vertical line at the counterfactual score
    plt.axvline(x=cf_score, color='#008ae7D2',
                linestyle='dashed', zorder=0)
    plt.text(cf_score - 0.10, len(text_features)*1.01 - 0.9,
             'Counterfactual Score', color='#008ae7D2')

    plt.gca().axes.get_yaxis().set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    # Plot classes names
    class_0_name = class_names[0]
    class_1_name = class_names[1]
    size_factual_class = mpl.textpath.TextPath(
        (0, 0), class_0_name).get_extents().width * 0.002
    plt.text(0.48 - size_factual_class - max([len(f) for f in text_features])*0.0001,
             len(text_features) - 0.9 + len(text_features)*0.04, class_0_name, color='#ff0055D2', fontweight='bold')
    plt.text(0.49, len(text_features) - 0.9 + len(text_features)*0.04, '➜',
             color='#c20000', fontweight='bold')
    plt.text(0.51, len(text_features) - 0.9 + len(text_features)*0.04,
             class_1_name, color='#008ae7D2', fontweight='bold')

    # Plot Counterfactual lines
    for i in range(len(single_points)):
        x_0 = point_to_pred[i]
        x_1 = cf_score
        y_0 = i
        y_1 = cf_pred_x_1
        plt.plot([x_0, x_1], [y_0, y_1], color='k', zorder=0,
                 linewidth=1, alpha=0.15, linestyle='dotted')

    for points, x_value in mulitple_points_chart:
        for origin_point in points:
            x_0 = point_to_pred[origin_point]
            x_1 = x_value
            y_0 = origin_point
            y_1 = np.mean(points)

            plt.plot([x_0, x_1], [y_0, y_1], color='#e0e0e0',
                     zorder=0, linewidth=1, alpha=0.5)

    if save_path is not None:
        plt.savefig(save_path, bbox_inches='tight')
