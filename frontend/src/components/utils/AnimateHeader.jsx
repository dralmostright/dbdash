import React from "react";
import "./AnimatedHeader.css";

export function AnimatedHeader() {
  return (
    <div className="animated-header">
      <div className="animated-header__bg" />
      <div className="animated-header__content">
        <h1 className="animated-header__title">Infinite Animation</h1>
        <p className="animated-header__subtitle">Runs forever ✨</p>
      </div>
    </div>
  );
}
