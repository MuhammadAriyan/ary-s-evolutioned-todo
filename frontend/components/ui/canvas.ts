'use client';

let animationFrameId: number | null = null;
let particles: Particle[] = [];

interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  radius: number;
  opacity: number;
  color: string;
}

const colors = [
  'rgba(153, 41, 234, 0.6)',  // Purple
  'rgba(255, 95, 207, 0.5)',  // Magenta
  'rgba(250, 235, 146, 0.4)', // Gold
];

function createParticle(canvas: HTMLCanvasElement): Particle {
  return {
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    vx: (Math.random() - 0.5) * 0.3,
    vy: (Math.random() - 0.5) * 0.3,
    radius: Math.random() * 2 + 1,
    opacity: Math.random() * 0.5 + 0.2,
    color: colors[Math.floor(Math.random() * colors.length)],
  };
}

function drawParticle(ctx: CanvasRenderingContext2D, particle: Particle) {
  ctx.beginPath();
  ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
  ctx.fillStyle = particle.color;
  ctx.globalAlpha = particle.opacity;
  ctx.fill();
  ctx.globalAlpha = 1;
}

function updateParticle(particle: Particle, canvas: HTMLCanvasElement) {
  particle.x += particle.vx;
  particle.y += particle.vy;

  if (particle.x < 0) particle.x = canvas.width;
  if (particle.x > canvas.width) particle.x = 0;
  if (particle.y < 0) particle.y = canvas.height;
  if (particle.y > canvas.height) particle.y = 0;
}

export function renderCanvas() {
  const canvas = document.getElementById('canvas') as HTMLCanvasElement | null;
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  if (!ctx) return;

  const resizeCanvas = () => {
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
  };
  resizeCanvas();
  window.addEventListener('resize', resizeCanvas);

  const particleCount = Math.min(50, Math.floor((canvas.width * canvas.height) / 15000));
  particles = Array.from({ length: particleCount }, () => createParticle(canvas));

  function animate() {
    if (!ctx || !canvas) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    particles.forEach((particle) => {
      drawParticle(ctx, particle);
      updateParticle(particle, canvas);
    });

    particles.forEach((p1, i) => {
      particles.slice(i + 1).forEach((p2) => {
        const dx = p1.x - p2.x;
        const dy = p1.y - p2.y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < 120) {
          ctx.beginPath();
          ctx.moveTo(p1.x, p1.y);
          ctx.lineTo(p2.x, p2.y);
          ctx.strokeStyle = `rgba(153, 41, 234, ${0.15 * (1 - distance / 120)})`;
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      });
    });

    animationFrameId = requestAnimationFrame(animate);
  }

  animate();
}

export function stopCanvas() {
  if (animationFrameId !== null) {
    cancelAnimationFrame(animationFrameId);
    animationFrameId = null;
  }
  particles = [];
}
