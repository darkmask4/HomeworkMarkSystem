const canvas = document.querySelector('canvas');

canvas.width=window.innerWidth;
canvas.height=window.innerHeight;

const ctx = canvas.getContext('2d');

const snowNum = 70;

const snowArray=[]

const snowImg = new Image();
snowImg.src = '/static/snow.png';

class Snow{
    constructor(){
        this.x = Math.random()*canvas.width;
        this.y = (Math.random()*canvas.height*2)-canvas.height;
        this.width=Math.random()*15+25;
        this.height = Math.random()*12+20;
        this.opacity = Math.random();
        this.xspeed = Math.random()*2+1;
        this.yspeed = Math.random()+1.5;
        this.rotateSpeed = Math.random()*0.02;
    }

    draw(){
        if(this.x>canvas.width || this.y>canvas.height){
            this.x=-snowImg.width;
            this.y=(Math.random()*canvas.height*2)-canvas.height;
            this.rotate = Math.random();
            this.xspeed = Math.random()*2+1;
            this.yspeed = Math.random()+1.5;
            this.rotateSpeed = Math.random()*0.02;
            console.log(1);
        }
 console.log('Snowflake position:', this.x, this.y); 
        ctx.globalAlpha = this.opacity;
        ctx.drawImage(
            snowImg,
            this.x,
            this.y,
            this.width*(0.6+(Math.abs(Math.cos(this.rotate))/3)),
            this.width*(0.6+(Math.abs(Math.cos(this.rotate))/3))
        )
        
    }

   

    animate(){
        this.x += this.xspeed + mouseX * 5;
        this.y += this.yspeed + mouseX * 4;
        this.rotate += this.rotateSpeed;
        this.draw();
    }

}

function render(){
    ctx.clearRect(0,0,canvas.width,canvas.height);
    snowArray.forEach(snow => snow.animate());
    window.requestAnimationFrame(render);
}

snowImg.addEventListener('load',() => {
    for (let i=0;i<snowNum;i++){
        const snowFlake = new Snow();
        snowFlake.animate()
        snowArray.push(snowFlake);
    }
    render();
})

let mouseX = 0;

function touchHandler(e){
    mouseX = (e.clientX || e.touches[0].clientX)/window.innerWidth;
}

window.addEventListener('mousemove',touchHandler)