export function CommaParser(azString) {
    if (!azString) return [];
    return azString
      .split(",")
      .map(item => item.trim())
      .filter(item => item.length > 0);
  }
  
