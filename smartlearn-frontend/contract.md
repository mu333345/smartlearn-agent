# Contract for ai agent

## goal
页面美化

## input 
目标文件：

    smartlearn-frontend/src/App.jsx（当前已包含完整的功能逻辑，所有 JSX 结构已就位）。

    smartlearn-frontend/src/index.css（当前可能只有 Vite 默认的样式，或内容极少）。

现有行为：

    所有功能（上传、聊天、禁用、加载、错误、回答、Page chips）均已通过 2.6 验证。

    HTML 结构使用了语义化标签（form、label、input、button 等），但样式为浏览器默认值。

样式状态：页面在宽屏和窄屏下可能显示拥挤或对齐不良。

## expected output
对 CSS 文件进行最小化样式补充，使页面具备以下特征（但不强制使用特定设计风格）：

布局结构：

    内容居中，最大宽度控制在 760px 左右，两侧留白（适合阅读）。

    上传区和聊天区用卡片（白色背景 + 圆角 + 阴影/边框）分隔，视觉上有层次感。

表单元素：

    文件选择器（<input type="file">）和文本输入框有足够的 padding（内边距），点击区域友好。

    输入框聚焦时显示明显的边框高亮（例如蓝色外发光）。

按钮状态：

    正常状态：有背景色（例如蓝色），文字白色，圆角。

    悬停状态（:hover）：背景色加深。

    禁用状态（:disabled）：透明度降低至 0.55，光标变为 not-allowed。

状态反馈：

    加载文字（"上传中..." / "思考中..."）用醒目的颜色（如橙色或蓝色）显示，并可能带简单的旋转动画（可选）。

    错误提示（role="alert"）用红色背景或红色边框突出显示，文字颜色为深红。

    成功上传后显示的元数据（页数、字符数）用绿色或灰色徽章样式。

引用标签（Page chips）：

    每个页码显示为圆角矩形背景（例如浅蓝色背景 + 深蓝色文字），内边距适中，多个标签之间间距均匀。

响应式：

    在窄屏（如手机宽度 400px）下，所有内容不溢出，按钮和输入框宽度自适应。

字体与颜色：

    使用系统字体栈（如 system-ui, sans-serif），保持清晰可读。

    主背景色为浅灰（#f4f7fb），卡片为白色，文字为深色（#172033）。

⚠️ 关键约束：

    所有样式必须通过修改 index.css 或在 App.jsx 中添加 className 实现，不得使用内联 style 属性（除非是动态样式，如基于状态的简单颜色变化）。

    不得修改任何 JavaScript 逻辑（状态管理、事件处理、条件渲染、API 调用）。

## modify boundary
允许修改：

smartlearn-frontend/src/index.css（添加或替换样式规则）。

smartlearn-frontend/src/App.jsx（仅限于添加 className 属性到现有 JSX 元素，例如 <div className="card">，不得修改任何事件处理函数、状态逻辑或条件渲染）。

允许创建（可选）：

    smartlearn-frontend/src/App.css（如果希望样式与组件更接近，但推荐直接使用 index.css 保持简单。

绝对不允许触碰：

    src/api.js（完全不动）。

    src/main.jsx（不动）。

    smartlearn-backend/ 下的任何文件。

    package.json（不新增依赖）。

禁止的操作：

    不要引入任何 UI 库（如 MUI、Ant Design、Tailwind CSS）。

    不要修改按钮的 onClick 或状态更新的逻辑。

    不要重新排列 HTML 结构（如果结构不合理，应该先回 2.6 改，而不是在美化步骤中顺手改）。


## nongoals
不要添加动画库（如 Framer Motion）或复杂的 CSS 动画（除非是极简的旋转加载图标）。

不要改变字体（使用系统字体即可，不需要 Google Fonts）。

不要添加暗黑模式或主题切换。

不要添加背景图片、渐变或装饰性图形。

不要改变任何用户交互流程（如新增弹窗、提示框等）。

