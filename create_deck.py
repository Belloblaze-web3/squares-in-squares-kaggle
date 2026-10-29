"""Generate a professional 16:9 PDF deck for the Squares in Squares project."""
from pathlib import Path
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Rectangle, Polygon, FancyBboxPatch, Circle

OUT = Path(__file__).parent / "squares_in_squares_project_deck.pdf"
NAVY, INK, TEAL, AMBER, MUTED, WHITE, GRID = "#0B132B", "#17213C", "#28C2B8", "#F4B942", "#91A0B8", "#F7F9FC", "#D9E2EC"
plt.rcParams.update({"font.family":"DejaVu Sans", "axes.titleweight":"bold"})


def base(title, kicker, page):
    fig = plt.figure(figsize=(13.333, 7.5), facecolor=WHITE)
    ax = fig.add_axes([0,0,1,1]); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.add_patch(Rectangle((0,0),1,1,color=WHITE))
    ax.add_patch(Rectangle((0,0),0.018,1,color=TEAL))
    ax.text(0.065,0.92,kicker.upper(),fontsize=9,color=TEAL,weight="bold",va="top",ha="left")
    ax.text(0.065,0.855,title,fontsize=25,color=NAVY,weight="bold",va="top",ha="left")
    ax.text(0.94,0.92,f"{page:02d}",fontsize=10,color=MUTED,weight="bold",ha="right")
    return fig, ax


def footer(ax, text="Squares in Squares · Kaggle project"):
    ax.plot([0.065,0.94],[0.065,0.065],color=GRID,lw=0.8)
    ax.text(0.065,0.035,text,fontsize=8,color=MUTED,va="center")


def txt(ax,x,y,s,size=13,color=INK,weight="normal",ha="left",va="top",linespacing=1.35):
    ax.text(x,y,s,fontsize=size,color=color,weight=weight,ha=ha,va=va,linespacing=linespacing)


def cover():
    fig=plt.figure(figsize=(13.333,7.5),facecolor=NAVY); ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')
    ax.add_patch(Rectangle((0,0),1,1,color=NAVY))
    for x,y,a,c in [(0.74,0.65,0.18,TEAL),(0.84,0.56,-0.2,AMBER),(0.68,0.46,-0.08,"#5E6CE5"),(0.81,0.36,0.22,"#E16B8C"),(0.60,0.32,0.12,TEAL)]:
        w=0.14; h=0.14
        pts=[(-w/2,-h/2),(w/2,-h/2),(w/2,h/2),(-w/2,h/2)]
        co,si=math.cos(a),math.sin(a)
        p=[(x+co*px-si*py,y+si*px+co*py) for px,py in pts]
        ax.add_patch(Polygon(p,closed=True,facecolor=c,edgecolor=WHITE,lw=2,alpha=.95))
    ax.add_patch(Rectangle((0.06,0.10),0.012,0.80,color=TEAL))
    txt(ax,0.10,0.75,"PACKING SQUARES,",35,WHITE,"bold")
    txt(ax,0.10,0.67,"PROFESSIONALLY.",35,AMBER,"bold")
    txt(ax,0.10,0.51,"A validation-first optimization pipeline for Kaggle",16,"#D9E2EC")
    txt(ax,0.10,0.45,"From geometry constraints to a reproducible submission.",13,"#A8B6CC")
    txt(ax,0.10,0.16,"Python · SAT geometry · simulated annealing · CI · Kaggle",10,"#A8B6CC")
    return fig


def problem():
    fig,ax=base("The problem: pack more, waste less","01 · framing",1)
    txt(ax,.07,.72,"For each puzzle n, place n unit squares inside the smallest axis-aligned square.",17,NAVY,"bold")
    txt(ax,.07,.61,"Each square is described by a center (x, y) and a rotation angle θ.\nThe evaluator recomputes the enclosing side length L.",13,INK)
    ax.add_patch(FancyBboxPatch((.07,.25),.35,.23,boxstyle="round,pad=.012,rounding_size=.01",fc=NAVY,ec="none"))
    txt(ax,.095,.415,"score(n) = L / √n − 1",24,WHITE,"bold")
    txt(ax,.095,.30,"Lower is better · leaderboard sums all puzzles",11,"#C4D0E0")
    ax.add_patch(Rectangle((.56,.27),.27,.27,fill=False,ec=TEAL,lw=2))
    for i in range(3):
        for j in range(3):
            if (i,j)!=(2,2): ax.add_patch(Rectangle((.56+i*.09,.27+j*.09),.09,.09,fc=TEAL,ec=WHITE,lw=1))
    txt(ax,.56,.21,"A 3 × 3 container for 8 squares",11,MUTED)
    footer(ax)
    return fig


def architecture():
    fig,ax=base("A three-layer solver architecture","02 · system design",2)
    cols=[(.08,"GEOMETRY",TEAL,"Vertices\nSAT overlap\nBoundary checks"),(.37,"SOLVERS",AMBER,"Grid baseline\nRectangular layouts\nAnnealing"),(.66,"DELIVERY", "#5E6CE5","Streaming CSV\nSchema validator\nKaggle + GitHub")]
    for x,title,c,body in cols:
        ax.add_patch(FancyBboxPatch((x,.31),.24,.32,boxstyle="round,pad=.012,rounding_size=.02",fc=WHITE,ec=GRID,lw=1.2))
        ax.add_patch(Rectangle((x,.60),.24,.03,color=c))
        txt(ax,x+.025,.55,title,14,NAVY,"bold")
        txt(ax,x+.025,.49,body,12,INK,linespacing=1.55)
    for x in [.325,.615]:
        ax.annotate("",xy=(x+.02,.47),xytext=(x-.02,.47),arrowprops=dict(arrowstyle="->",lw=2,color=MUTED))
    txt(ax,.08,.77,"The professional move was to separate correctness from search.",17,NAVY,"bold")
    txt(ax,.08,.70,"Every optimization experiment must pass through the same geometry and delivery gates.",12,MUTED)
    footer(ax)
    return fig


def geometry():
    fig,ax=base("Constraint engineering: prove validity","03 · geometry",3)
    txt(ax,.07,.73,"Rotated squares are convex polygons—so the Separating Axis Theorem gives a clean test.",16,NAVY,"bold")
    # diagram
    ax.add_patch(Rectangle((.08,.23),.33,.33,fill=False,ec=GRID,lw=1.5))
    p1=[(.15,.30),(.30,.30),(.30,.45),(.15,.45)]
    p2=[(.27,.31),(.40,.39),(.33,.52),(.20,.44)]
    ax.add_patch(Polygon(p1,fc=TEAL,ec=WHITE,lw=2,alpha=.9)); ax.add_patch(Polygon(p2,fc=AMBER,ec=WHITE,lw=2,alpha=.9))
    txt(ax,.08,.17,"Positive-area overlap → reject\nEdge/corner touch → allowed",11,MUTED)
    items=[("1","Compute vertices from (x, y, θ)"),("2","Project both polygons on each edge normal"),("3","A separating axis proves non-overlap")]
    for i,(n,s) in enumerate(items):
        y=.57-i*.14
        ax.add_patch(Circle((.56,y),.025,fc=TEAL)); txt(ax,.56,y-.002,n,11,WHITE,"bold","center","center"); txt(ax,.61,y+.02,s,13,INK,"bold")
    txt(ax,.56,.13,"Boundary checks use the actual rotated vertices, not just centers.",11,MUTED)
    footer(ax)
    return fig


def baseline():
    fig,ax=base("Start with a strong, safe baseline","04 · baseline",4)
    txt(ax,.07,.73,"A complete baseline is more valuable than an incomplete clever idea.",17,NAVY,"bold")
    txt(ax,.07,.65,"For each n, choose the best near-square integer rectangle and place one square per cell.",12,INK)
    # grid visual
    for i in range(5):
        for j in range(4):
            if not (i==4 and j>1): ax.add_patch(Rectangle((.10+i*.065,.27+j*.065),.065,.065,fc=TEAL if (i+j)%2 else "#A8E5E0",ec=WHITE,lw=1))
    txt(ax,.10,.20,"18 squares → 5 × 4 container",11,MUTED)
    metrics=[("1,000","puzzles covered"),("500,500","data rows"),("0°","rotation in fallback")]
    for i,(big,small) in enumerate(metrics):
        x=.53+i*.14
        txt(ax,x,.47,big,23,NAVY,"bold")
        txt(ax,x,.39,small,10,MUTED)
    txt(ax,.53,.23,"The baseline is deterministic, cheap, explainable, and always available when a heuristic search fails.",12,INK)
    footer(ax)
    return fig


def optimization():
    fig,ax=base("Improve selectively with annealing","05 · search",5)
    txt(ax,.07,.73,"Simulated annealing explores continuous centers and angles without sacrificing the fallback.",16,NAVY,"bold")
    steps=[("START","rectangular layout"),("PERTURB","move one square / rotate"),("SCORE","container side + penalties"),("KEEP","accept improvement or escape local minima")]
    for i,(h,b) in enumerate(steps):
        x=.08+i*.21
        ax.add_patch(Circle((x+.06,.47),.045,fc=AMBER if i==1 else TEAL,ec="none"))
        txt(ax,x+.06,.47,str(i+1),14,NAVY,"bold","center","center")
        txt(ax,x,.36,h,11,NAVY,"bold")
        txt(ax,x,.30,b,10,INK)
        if i<3: ax.annotate("",xy=(x+.20,.47),xytext=(x+.12,.47),arrowprops=dict(arrowstyle="->",lw=1.8,color=MUTED))
    ax.add_patch(FancyBboxPatch((.08,.12),.78,.09,boxstyle="round,pad=.01",fc="#EAF7F6",ec="none"))
    txt(ax,.10,.165,"Engineering rule: optimize small puzzle sizes first; retain the validated deterministic layout for everything else.",11,NAVY,"bold")
    footer(ax)
    return fig


def results():
    fig,ax=base("What shipped","06 · results",6)
    txt(ax,.07,.73,"The pipeline produced a complete, validated, and submitted artifact.",17,NAVY,"bold")
    data=[("500,500","submission rows"),("1,000","puzzles"),("28.9377","local baseline score"),("VALID","geometry gate")]
    for i,(big,small) in enumerate(data):
        x=.08+(i%2)*.42; y=.50-(i//2)*.22
        ax.add_patch(Rectangle((x,y),.31,.14,fc=NAVY if i==3 else "#F1F5F9",ec="none"))
        txt(ax,x+.025,y+.095,big,22,WHITE if i==3 else TEAL,"bold")
        txt(ax,x+.025,y+.04,small,10,WHITE if i==3 else MUTED)
    txt(ax,.08,.18,"Kaggle accepted submission.csv and queued it for evaluation.",13,INK,"bold")
    footer(ax)
    return fig


def lessons():
    fig,ax=base("Lessons for practical optimization","07 · takeaways",7)
    lessons=[("01","Separate correctness from search."),("02","Make the baseline complete and reproducible."),("03","Use exact geometry where invalidity is expensive."),("04","Deliver the whole workflow: tests, CI, artifacts, and provenance.")]
    for i,(n,s) in enumerate(lessons):
        y=.68-i*.13
        txt(ax,.09,y,n,12,TEAL,"bold")
        txt(ax,.17,y,s,17,NAVY,"bold")
        ax.plot([.17,.88],[y-.035,y-.035],color=GRID,lw=.8)
    txt(ax,.09,.13,"Next step: replace the baseline with stronger search while preserving the same validation gates.",12,MUTED)
    footer(ax,"Squares in Squares · github.com/Belloblaze-web3/squares-in-squares-kaggle")
    return fig


def main():
    pages=[cover,problem,architecture,geometry,baseline,optimization,results,lessons]
    with PdfPages(OUT) as pdf:
        for fn in pages: pdf.savefig(fn(),facecolor=WHITE,bbox_inches=None); plt.close('all')
    print(OUT)

if __name__ == "__main__": main()
