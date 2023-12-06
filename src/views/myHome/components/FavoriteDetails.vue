<!-- HTML结构 -->
<button id="add-btn">添加收藏</button>
<ul id="list"></ul>

<!-- JavaScript代码 -->
<script>
const addBtn = document.getElementById('add-btn');
const list = document.getElementById('list');

// 获取收藏列表
const getFavorites = async () => {
  const response = await fetch('/api/favorites');
  const data = await response.json();
  return data.favorites;
}

// 渲染收藏列表
const renderFavorites = async () => {
  const favorites = await getFavorites();
  list.innerHTML = '';
  favorites.forEach(favorite => {
    const li = document.createElement('li');
    li.textContent = favorite;
    list.appendChild(li);
  });
}

// 添加收藏
addBtn.addEventListener('click', async () => {
  const favorite = prompt('请输入收藏内容：');
  if (favorite) {
    await fetch('/api/favorites', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ favorite })
    });
    renderFavorites();
  }
});

// 页面加载时渲染收藏列表
renderFavorites();
</script>
