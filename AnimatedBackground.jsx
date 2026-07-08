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
                    zIndex: -1
                },

                background: {
                    color: {
                        value: "transparent"
                    }
                },

                fpsLimit: 60,

                particles: {
                    number: {
                        value: 54
                    },

                    color: {
                        value: ["#64d4c8", "#68a7ff"]
                    },

                    links: {
                        enable: true,
                        distance: 150,
                        color: "#5dbbd8",
                        opacity: 0.18,
                        width: 1
                    },

                    move: {
                        enable: true,
                        speed: 0.55,
                        outModes: {
                            default: "bounce"
                        }
                    },

                    opacity: {
                        value: 0.34
                    },

                    size: {
                        value: {
                            min: 1,
                            max: 3
                        }
                    }
                },

                detectRetina: true
            }}
        />
    );
}
