const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];

/* Drawer ya kushoto */
const drawer=$('#drawer'),scrim=$('#scrim'),openBtn=$('#open');
if(drawer){
  const toggle=o=>{drawer.classList.toggle('open',o);scrim.classList.toggle('on',o);
    document.body.style.overflow=o?'hidden':'';openBtn.setAttribute('aria-expanded',o?'true':'false')};
  openBtn.onclick=()=>toggle(true);$('#close').onclick=()=>toggle(false);scrim.onclick=()=>toggle(false);
  $$('.dnav a').forEach(a=>a.onclick=()=>toggle(false));
  addEventListener('keydown',e=>e.key==='Escape'&&toggle(false));
}

/* Slideshow yoyote yenye .stage — inaanza tu ikiwa inaonekana */
function slideshow(stage){
  const s=[...stage.querySelectorAll('.sl')];if(s.length<2)return;
  const ms=+stage.dataset.show||6000,delay=+stage.dataset.delay||0;
  const dotBox=stage.dataset.dots?document.getElementById(stage.dataset.dots):null;
  if(dotBox)dotBox.innerHTML=s.map((_,i)=>`<span class="${i?'':'on'}"></span>`).join('');
  const dots=dotBox?[...dotBox.children]:[];
  let i=0,t=null;
  const step=()=>{s[i].classList.remove('on');dots[i]&&dots[i].classList.remove('on');
    i=(i+1)%s.length;s[i].classList.add('on');dots[i]&&dots[i].classList.add('on')};
  new IntersectionObserver(es=>es.forEach(e=>{
    if(e.isIntersecting){if(!t)t=setTimeout(()=>{step();t=setInterval(step,ms)},delay+ms)}
    else{clearInterval(t);clearTimeout(t);t=null}}),{threshold:.05}).observe(stage);
  stage._go=n=>{s[i].classList.remove('on');i=n;s[i].classList.add('on')};
}
$$('.stage').forEach(slideshow);

/* Hero: picha, vidoti na maandishi vinabadilika pamoja */
const heroStage=$('.hero .stage'),hdots=$$('.dot'),txt=$('#txt');
if(heroStage&&hdots.length>1){
  const copy=$$('#hero-copy > div').map(d=>[d.dataset.h,d.dataset.p]);
  let hc=0,ht;
  const paint=n=>{hdots[hc].classList.remove('on');hc=n;hdots[hc].classList.add('on');
    heroStage._go&&heroStage._go(hc);
    if(copy[hc]){txt.classList.remove('on');void txt.offsetWidth;
      $('#hh').textContent=copy[hc][0];$('#hp').textContent=copy[hc][1];txt.classList.add('on')}};
  const run=()=>ht=setInterval(()=>paint((hc+1)%hdots.length),7000);
  run();
  hdots.forEach(d=>d.onclick=()=>{clearInterval(ht);paint(+d.dataset.i);run()});
}

/* Sections zinaingia zikipanda */
const io=new IntersectionObserver(es=>es.forEach(e=>{
  if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.15});
$$('.rev').forEach(el=>io.observe(el));

/* Mstari wa bidhaa */
const rail=$('#rail');
if(rail){$('#next').onclick=()=>rail.scrollBy({left:320,behavior:'smooth'});
  $('#prev').onclick=()=>rail.scrollBy({left:-320,behavior:'smooth'})}

/* Maswali */
$$('.q button').forEach(b=>b.onclick=()=>{
  const q=b.parentElement,a=q.querySelector('.a'),open=q.classList.contains('open');
  $$('.q').forEach(o=>{o.classList.remove('open');o.querySelector('.a').style.maxHeight=null});
  if(!open){q.classList.add('open');a.style.maxHeight=a.scrollHeight+'px'}});

/* Navbar, mstari wa maendeleo na parallax */
const bar=$('#bar'),prog=$('#prog'),bandArt=$('.band .art'),heroArt=$('.hero .art');
addEventListener('scroll',()=>{
  if(bar)bar.classList.toggle('solid',scrollY>(heroArt?innerHeight-90:60));
  if(prog)prog.style.width=(scrollY/(document.body.scrollHeight-innerHeight)*100)+'%';
  if(heroArt&&scrollY<innerHeight)heroArt.style.transform='translateY(calc(-50% + '+(scrollY*.16)+'px))';
  if(bandArt){const r=bandArt.getBoundingClientRect();
    if(r.top<innerHeight&&r.bottom>0)
      bandArt.style.transform='translate(-50%,calc(-50% + '+((innerHeight/2-r.top-r.height/2)*.07)+'px))'}
},{passive:true});

/* Picha kuu ya bidhaa inabadilika kwa thumbnail */
const mainImg=$('[data-main-image]');
if(mainImg)$$('[data-thumb]').forEach(t=>t.onclick=()=>mainImg.src=t.dataset.thumb);
