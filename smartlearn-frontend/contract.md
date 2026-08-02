# Contract for ai agent

## goal
Learn Component State


## input 
目标文件：smartlearn-frontend/src/App.jsx。

现有状态：该文件目前是一个最简的 Vite + React 起始页（通常只包含一个 <h1> 标题或 Vite 图标），没有任何业务状态或交互逻辑。

前提条件：npm install 已执行，npm run dev 能正常打开页面。

## expected output
代码变动：在 App.jsx 中最小化新增以下内容（且只新增这些）：

    导入 useState（如果尚未导入）；

    添加一个状态变量 status，初始值为 "Not uploaded"；

    在 JSX 中渲染该状态（例如 <p>Status: {status}</p>）；

    添加一个按钮，点击后将 status 更新为 "Ready"。

运行时表现：启动 Vite 后，页面显示状态文本和按钮。点击按钮，页面上的文字从 "Not uploaded" 变为 "Ready"，浏览器不刷新。

最终清理（关键）：在我学会并确认循环机制后，我会要求你仅移除上述临时实验代码，并确保 App.jsx 恢复为有效的起始页（或保留后续开发所需的空壳），不得留下任何死代码或注释。

## modify boundary
允许修改：
    只允许修改 smartlearn-frontend/src/App.jsx 这一个文件。

绝对不允许触碰：

    src/main.jsx、src/index.css；

    package.json、vite.config.js、eslint.config.js；

    项目根目录及后端（smartlearn-backend/）下的任何文件；

    禁止新增任何额外的 .css 类或样式标签（实验不带样式）。

## nongoals
不要添加第二个状态变量或副作用（useEffect）。

不要修改按钮样式或布局（保持原生 HTML 按钮外观即可）。

不要让这个实验代码成为永久功能——本次实验是临时插入的，后续必须干净移除。

不要在这个实验中引入 API 请求、路由跳转或复杂逻辑。