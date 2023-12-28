!(function(){

    var canvas = document.createElement("canvas");
    document.body.appendChild(canvas);

    canvas.style.position = "fixed";
    canvas.style.left = "0";
    canvas.style.top = "0";
    canvas.style.zIndex = -1;
    
    var context = canvas.getContext("2d");

    function resizeCanvas(){
        canvas.width=window.innerWidth;
        canvas.height=window.innerHeight;

    //    clearCanvas();
    }

    function clearCanvas(){
    //    context.fillStyle="rgba(255, 255, 255, 0.1)";
    //    context.fillRect(0,0,canvas.width,canvas.height);
    }

    resizeCanvas();
    window.addEventListener("resize",resizeCanvas);

    function drawRandomFirework() {
        var x = Math.random() * canvas.width;
        var y = Math.random() * canvas.height;

        createFirework(x, y);
    }

    setInterval(drawRandomFirework, 1500*Math.random());

    var suoyou = [];
    function createFirework(x,y){
        var count = Math.random()*200;
        var radius = 10;

        var hue = Math.floor(Math.random()*51)+150;
        var huebianhua = 300*Math.random();
        
        for(var i = 0;i<count;i++){
            var angle = 360/count*i;
            var radians = angle * Math.PI/180;

            var p ={};

            p.x=x;
            p.y=y;
            p.radians=radians;
            
            p.size=2;

            p.hue = Math.floor(Math.random()*((hue + huebianhua)-(hue-huebianhua)))+(hue-huebianhua);
            p.brightness = Math.floor(Math.random()*31)+50;
            p.alpha = (Math.floor(Math.random()*61)+40)/100;

            p.speed = (Math.random()*5)+.4;
            p.radius=p.speed;
            suoyou.push(p);
        }
    }

    function drawFirework(){

        for(var i=0;i<suoyou.length;i++){
            var p = suoyou[i];

            var vx = Math.cos(p.radians)*p.radius;
            var vy = Math.sin(p.radians)*p.radius + 0.4;
            p.x += vx;
            p.y += vy;

            p.radius *=1-p.speed/100;

            p.alpha -=0.01;

            if(p.x<0 || p.x>canvas.width ||p.y<0 ||p.y>canvas.height || p.alpha<=0){
                suoyou.splice(i,1);

                continue;
            }

            context.beginPath();
            context.arc(p.x,p.y,p.size,0,Math.PI*2,false);

            context.closePath();

            context.fillStyle = 'hsla('+p.hue+',100%,'+p.brightness+'%,'+p.alpha+')';
            context.fill();
        }


    }


    function tick(){
        context.globalCompositeOperation = 'destination-out';
        context.fillStyle = 'rgba(255,255,255,'+10/100+')';
        context.fillRect(0,0,canvas.width,canvas.height);
        context.globalCompositeOperation = 'lighter';
        drawFirework();
        requestAnimationFrame(tick);
    }

    tick();
})();