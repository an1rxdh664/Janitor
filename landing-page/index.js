const GRID_DATA = [
      [0,0,2,1,1,1,1,1,2,1],
      [0,1,1,1,3,2,1,1,3,2],
      [0,0,1,1,3,2,1,1,1,2],
      [0,0,0,3,3,2,1,1,2,1],
      [0,0,0,0,2,1,3,3,2,1],
      [0,0,0,1,1,2,1,3,1,1],
      [0,0,3,2,1,1,1,3,1,2],
      [0,1,1,3,2,1,1,1,3,2],
      [1,3,2,2,3,2,1,3,2,3],
      [2,2,1,1,2,1,2,1,3,3],
    ];

    const SHADES = { 0: null, 1: '#1a3d2b', 2: '#2ecc71', 3: '#39d353' };

    const grid = document.getElementById('pixel-grid');
    GRID_DATA.forEach(row => {
      const rowEl = document.createElement('div');
      rowEl.className = 'pixel-row';
      row.forEach(val => {
        const cell = document.createElement('div');
        cell.className = 'pixel';
        if (SHADES[val]) cell.style.backgroundColor = SHADES[val];
        rowEl.appendChild(cell);
      });
      grid.appendChild(rowEl);
    });