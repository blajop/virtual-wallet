import React, { useEffect, useRef, useState } from "react";

interface ScrollContainerProps {
  children: React.ReactNode[];
}

const ScrollContainer: React.FC<ScrollContainerProps> = ({ children }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [activeIndex, setActiveIndex] = useState(0);

  useEffect(() => {
    const handleScroll = () => {
      if (containerRef.current) {
        const { scrollTop, clientHeight } = containerRef.current;
        const newIndex = Math.floor(scrollTop / clientHeight);
        setActiveIndex(newIndex);
      }
    };

    const container = containerRef.current;

    if (container) {
      container.addEventListener("scroll", handleScroll);
    }

    return () => {
      if (container) {
        container.removeEventListener("scroll", handleScroll);
      }
    };
  }, []);

  useEffect(() => {
    if (containerRef.current) {
      const container = containerRef.current;
      const activeComponent = container.children[activeIndex] as HTMLElement;
      container.scrollTo({
        top: activeComponent.offsetTop,
        behavior: "smooth",
      });
    }
  }, [activeIndex]);

  return (
    <div style={{ height: "100vh", overflow: "auto" }} ref={containerRef}>
      <div style={{ height: `${children.length * 100}vh` }}>
        {children.map((child, index) => (
          <div key={index} style={{ height: "100vh" }}>
            {child}
          </div>
        ))}
      </div>
    </div>
  );
};

export default ScrollContainer;
