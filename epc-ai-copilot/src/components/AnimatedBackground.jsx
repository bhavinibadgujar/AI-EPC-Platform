import Particles from "@tsparticles/react";
import { loadSlim } from "@tsparticles/slim";
import { useCallback } from "react";

export default function AnimatedBackground() {
  const particlesInit = useCallback(async (engine) => {
    await loadSlim(engine);
  }, []);

  return (
    <Particles
      id="tsparticles"
      init={particlesInit}
      options={{
        fullScreen: {
          enable: true,
          zIndex: -1,
        },

        background: {
          color: {
            value: "transparent",
          },
        },

        fpsLimit: 60,

        interactivity: {
          events: {
            onHover: {
              enable: false,
            },
            onClick: {
              enable: false,
            },
            resize: true,
          },
        },

        particles: {
          number: {
            value: 42,
            density: {
              enable: true,
              area: 900,
            },
          },

          color: {
            value: ["#64d4c8", "#68a7ff"],
          },

          links: {
            enable: true,
            distance: 160,
            color: "#64d4c8",
            opacity: 0.12,
            width: 1,
          },

          move: {
            enable: true,
            speed: 0.4,
            outModes: {
              default: "bounce",
            },
          },

          opacity: {
            value: 0.25,
          },

          size: {
            value: {
              min: 1,
              max: 2.5,
            },
          },
        },

        detectRetina: true,
      }}
    />
  );
}