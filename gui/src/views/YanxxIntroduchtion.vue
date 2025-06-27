<template>
  <div class="profile-container">
    <!-- 头部区域 -->
    <header class="profile-header">
      <h1>这里是 <span class="emphasize">严小希</span> 的自我介绍<small class="decorative">qwq</small></h1>
      <p class="greeting">你好呀，我叫<code>严小希</code>，是一位就读于人小附大的高三学生。</p>
    </header>

    <!-- 好友介绍区域 -->
    <section class="friend-note">
      <h3>简短的介绍后，<span class="emphasize">严小希</span>又埋头去做无穷无尽的物理卷子了呢</h3>
      <p>于是乎，就让我，<span class="emphasize">严小希</span>的好友<span class="emphasize">xiaoce</span>来接着替她介绍一下吧～</p>
    </section>

    <!-- 主体内容 -->
    <main class="profile-content">
      <!-- 基本信息卡片 -->
      <div class="info-card">
        <p>🎓 <span class="emphasize">严小希</span>将在今年6月份参加高考并毕业，她一直梦想考入<span class="emphasize">北京大学</span>。在学校中，<span class="emphasize">严小希</span>以其阳光可爱、积极向上的性格在校园内外广受好评。她不仅学业优秀，还十分的可爱。</p>
        <p><span class="emphasize">严小希</span>非常喜欢<span class="emphasize">泡泡</span>老师，也因此非常的喜欢<span class="emphasize">物理</span>。欢迎向小希请教物理问题哦~</p>
      </div>

      <!-- 外貌模块 -->
      <section class="feature-section">
        <div class="image-container">
          <img src="../../pictures/yanxx/pic1.png" alt="严小希形象图" class="profile-image">
        </div>
        <div class="feature-list">
          <h2>外貌</h2>
          <ul>
            <li><span class="feature-label">头发：</span>拥有一头柔软顺滑的浅棕色长发，常以半扎马尾或自然散落的发型示人，额前轻盈的刘海增添了几分俏皮感。</li>
            <li><span class="feature-label">眼睛：</span>明亮的琥珀色眼眸，闪烁着好奇与智慧的光芒，笑起来时会弯成月牙形，给人以温暖亲切的感觉。</li>
            <li><span class="feature-label">服装：</span>偏好简约而不失个性的装扮。日常穿着以人大附中的红白校服为主</li>
          </ul>
        </div>
      </section>

      <!-- 性格模块 -->
      <section class="personality-section">
        <h2>性格</h2>
        <div class="grid-container">
          <div class="trait-card" v-for="(trait, index) in traits" :key="index">
            <h3>{{ trait.title }}</h3>
            <p>{{ trait.description }}</p>
          </div>
        </div>
      </section>

      <!-- 作品模块 -->
      <section class="works-section">
        <h2>作品</h2>
        <div class="work-links">
          <a v-for="(work, index) in works" 
             :key="index" 
             :href="work.url" 
             :title="work.tip"
             class="work-link">
            📚 {{ work.title }}
          </a>
        </div>
      </section>
    </main>

    <!-- 后记 -->
    <footer class="postscript">
      <p>感谢 <a herf="https://github.com/xiaoce-2025/">xiaoce-2025</a> 与 <a herf="https://github.com/firefly1145141919810/">firefly1145141919810</a> 对此项目做出的贡献～</p>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'


const traits = ref([
  {
    title: '可爱，幽默，活泼乐观开朗',
    description: '小希总是以积极的态度面对生活中的挑战，她的笑声仿佛有魔力，能瞬间驱散周围的阴霾。'
  },
  {
    title: '好奇探索',
    description: '对未知世界充满无限好奇，无论是物理世界的新技术，还是虚拟空间的无限可能，都激发着她不断探索的欲望。'
  },
  {
    title: '创新创造',
    description: '擅长将想法转化为现实，无论是编程、设计还是艺术创作，都能展现出非凡的创造力和执行力。'
  },
  {
    title: '乐于助人',
    description: '乐于助人，善于倾听朋友的心声，经常用自己的知识和经验帮助他人解决问题，是大家公认的小太阳。'
  },
  // 其他性格特征...
])

const works = ref([
  {
    title: '摸鱼摸鱼-劝学改',
    url: 'https://mp.weixin.qq.com/s/aFtVIvBagQb8WW-1eEJM6A',
    tip: '这是严小希非常满意的一篇作品哦～'
  },
  {
    title: '槐时量子雨',
    url: 'https://mp.weixin.qq.com/s/ohLAoCAYIK1saX5pGgQvfw',
    tip: '连载中，这是第三篇～'
  },
])
</script>

<style lang="scss" scoped>
.profile-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 0rem;
  font-family: 'Microsoft YaHei', sans-serif;
  color: #333;

  .emphasize {
    color: #7c4dff;
    font-weight: 600;
  }

  .profile-header {
    text-align: center;
    h1 {
      font-size: 2.2rem;
      .decorative {
        color: #ff6b6b;
        margin-left: 0.5rem;
      }
    }
  }

  .friend-note {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 12px;
    margin: 2rem 0;
  }

  .feature-section {
    display: flex;
    gap: 2rem;
    margin: 2rem 0;

    .image-container {
      flex: 1;
      img {
        width: 100%;
        max-width: 300px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      }
    }

    .feature-list {
      flex: 2;
      .feature-label {
        color: #7c4dff;
        font-weight: 500;
      }
    }
  }

  .trait-card {
    background: white;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    transition: transform 0.2s;

    &:hover {
      transform: translateY(-4px);
    }
  }

  .work-link {
    display: block;
    padding: 1rem;
    background: #f3e5f5;
    border-radius: 6px;
    margin: 0.5rem 0;
    transition: background 0.2s;

    &:hover {
      background: #e1bee7;
    }
  }

  .postscript {
    margin-top: 3rem;
    font-size: 0.9rem;
    color: #666;
    text-align: center;
  }
}
</style>
  