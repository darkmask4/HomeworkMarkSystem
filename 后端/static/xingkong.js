let canvas = document.createElement("canvas")
canvas.style.position = "fixed";
canvas.style.top = "0";
canvas.style.left = "0";
canvas.style.width = "100%";
canvas.style.height = "100%";
canvas.style.zIndex = "-1";
canvas.style.pointerEvents = "none"; // 防止<canvas>元素干扰鼠标事件
canvas.width = window.innerWidth
canvas.height = window.innerHeight
canvas.style.zIndex=-1
let ctx = canvas.getContext("2d")
document.body.appendChild(canvas)
let particles = []
let pcount = 1000



class particle{
    constructor(){
        this.x=Math.random() * canvas.width
        this.y=Math.random() * canvas.height
        this.vx = Math.random()
    }
    update(){
        this.x += this.vx*3
        if (this.x>canvas.width){
            this.x=0
        }
    }
    draw() {
        ctx.beginPath()
        ctx.arc(this.x,this.y,1+this.vx,0,Math.PI*2)
        ctx.fillStyle = "rgba(255,255,255," + this.vx +")"
        ctx.fill()
    }
}

function ani(){
    ctx.clearRect(0,0,canvas.width,canvas.height)
    if(particles.length<pcount){
        particles.push(new particle)
    }
    for(let i in particles){
        let p = particles[i]
        p.update()
        p.draw()
    }
}

setInterval(ani,100/6)