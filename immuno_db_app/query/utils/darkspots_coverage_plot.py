import base64
import gzip

import plotly.graph_objects as go
import plotly.io as pio

from django.urls import reverse
from urllib.parse import urlencode

LETTER_ZOOM_MIN_PX = 8

# Button *size* is defined in css ( .modebar-btn)
MODEBAR_CONFIG = {
    'scrollZoom': True,
    'displaylogo': False,
    'modeBarButtonsToRemove': ['select2d', 'lasso2d', 'toImage'],
}


LETTER_ZOOM_JS = r"""
window.darkspotsLetterZoom = function (gd, minPx) {
    minPx = minPx || 8;
    var li = -1, shown = null, pending = false;
    for (var i = 0; i < gd.data.length; i++)
        if (gd.data[i].mode === 'text') { li = i; break; }

    function apply() {
        pending = false;
        if (li < 0) return;
        var xa = gd._fullLayout && gd._fullLayout.xaxis;
        if (!xa || !xa.range) return;
        var span = xa.range[1] - xa.range[0];
        // xa._length is the axis width in px, so this is screen-width aware:
        // a fixed residue-count threshold would over/under-show depending
        // on the monitor (and on how wide the app's column happens to be).
        var show = span > 0 && xa._length / span >= minPx;
        if (show === shown) return;
        shown = show;
        Plotly.restyle(gd, {visible: show}, [li]);
    }

    function schedule() {
        if (pending) return;
        pending = true;
        requestAnimationFrame(apply);
    }

    gd.on('plotly_relayout', function (e) {
        for (var k in e)
            if (k.indexOf('xaxis.range') === 0 || k === 'xaxis.autorange'
                || k === 'autosize' || k === 'width') { schedule(); return; }
    });
    window.addEventListener('resize', schedule);

    apply();
    return apply;
};
"""


def hide_letter_trace(fig, visible=False):
    for trace in fig.data:
        if getattr(trace, 'mode', None) == 'text':
            trace.visible = visible
    return fig


def figure_from_gz_b64(figure_json_gz_b64):
    """Restore the Figure from the gzipped, base64-encoded JSON in the DB."""
    return pio.from_json(
        gzip.decompress(base64.b64decode(figure_json_gz_b64)).decode())


def coverage_plot_div(figure,
                      min_px_per_residue=LETTER_ZOOM_MIN_PX,
                      include_plotlyjs='cdn', div_id=None):
    """Render the coverage plot as an HTML fragment.

    `figure` is either a Figure (so callers can annotate it first) or the
    stored gzipped/base64 figure JSON.
    """
    fig = figure if isinstance(figure, go.Figure) else figure_from_gz_b64(figure)
    hide_letter_trace(fig)
    js = LETTER_ZOOM_JS + (
        "\ndarkspotsLetterZoom(document.getElementById('{plot_id}'), %d);\n"
        % min_px_per_residue)
    return pio.to_html(fig, full_html=False,
                       include_plotlyjs=include_plotlyjs,
                       post_script=js, config=dict(MODEBAR_CONFIG),
                       div_id=div_id)


PEPTIDE_HIGHLIGHT_COLOR = 'rgba(255, 215, 0, 0.22)'
PEPTIDE_LEGEND_COLOR = 'rgba(255, 215, 0, 0.75)'

def add_peptide_highlight(fig, start, end, color=PEPTIDE_HIGHLIGHT_COLOR):
    # 'between' puts the band above the figure's own background regions but
    # below the traces -- 'above' would tint every bar it covers.
    fig.add_shape(type='rect', xref='x', yref='paper',
                  x0=start - 0.5, x1=end + 0.5, y0=0, y1=1,
                  fillcolor=color, line=dict(width=0), layer='between')
    return fig

def add_swatch_legend_entry(fig, label, color, legend='legend5', legendrank=50):
    """Add an invisible trace whose only purpose is a colored legend swatch."""
    fig.add_trace(go.Scattergl(x=[None], y=[None], mode='lines',
                               line=dict(color=color, width=10),
                               name=label, legend=legend, legendrank=legendrank,
                               showlegend=True, hoverinfo='skip'))
    return fig


def add_highlight_legend_entry(fig, label, color=PEPTIDE_LEGEND_COLOR,
                               legend='legend5', legendrank=50):
    return add_swatch_legend_entry(fig, label, color, legend=legend,
                                   legendrank=legendrank)


def sequence_from_figure(fig):
    for trace in fig.data:
        if getattr(trace, 'mode', None) == 'text' and trace.text is not None:
            return ''.join(trace.text)
    raise ValueError("figure has no letter trace (built without sequence=...)")


def find_peptide_positions(sequence, peptide):
    spans = []
    index = sequence.find(peptide)
    while index != -1:
        spans.append((index + 1, index + len(peptide)))
        index = sequence.find(peptide, index + 1)
    return spans


def highlight_peptide(fig, peptide, sequence=None, color=PEPTIDE_HIGHLIGHT_COLOR,
                      label=None, legend='legend5'):
    if not peptide:
        return []

    if sequence is None:
        sequence = sequence_from_figure(fig)

    spans = find_peptide_positions(sequence, peptide)
    for start, end in spans:
        add_peptide_highlight(fig, start, end, color=color)

    if spans:
        if label is None:
            label = peptide if len(spans) == 1 else f'{peptide} ({len(spans)} sites)'
        add_highlight_legend_entry(fig, label, legend=legend)

    return spans


def sibling_protein_links(psm, current_accession, database):
    """Links to every protein the psm's peptide maps to, for the dropdown."""
    query = urlencode({'database': database, 'psm': psm.pk})
    return [{'accession': accession,
             'name': name,
             'url': f"{reverse('protein', kwargs={'uniprot_code': accession})}?{query}",
             'is_current': accession == current_accession}
            for accession, name in psm.proteins_by_name()]
