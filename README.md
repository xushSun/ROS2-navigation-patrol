# ROS2_navigation_patrol

本项目为基于 ROS2 的自主巡逻/导航机器人系统，适用于 SLAM、路径规划、导航与多传感器集成等场景。

## 目录结构

- `src/`：源代码目录，包含各功能包（如 slam、navigation、robot description 等）
- `build/`、`install/`、`log/`：构建、安装和日志输出目录（已在 `.gitignore` 中忽略）

## 主要功能包

- `autopatrol_interface/`：自定义消息与服务接口
- `autopatrol_robot/`：机器人底盘驱动与硬件接口
- `demo_cpp_slam/`：SLAM 示例包
- `guobot_application/`：应用层逻辑
- `guobot_description/`：机器人 URDF/Xacro 及相关描述文件
- `guobot_navigation2/`：导航2功能包

## 环境依赖

- ROS2（建议使用 Humble 版本，需与实际环境一致）
- colcon（ROS2 构建工具）
- 其他依赖包请参考各功能包下的 `package.xml` 和 `CMakeLists.txt`

## 编译与运行

1. 安装依赖

   ```bash
   sudo apt update
   rosdep install --from-paths src --ignore-src -r -y
   ```

2. 编译工作空间

   ```bash
   colcon build --symlink-install
   ```

3. 加载环境

   ```bash
   source install/setup.bash
   ```

4. 启动相关节点（以导航为例）

   ```bash
   ros2 launch guobot_navigation2 bringup_launch.py
   ```

## 贡献指南

1. Fork 本仓库并新建分支
2. 提交代码前请确保通过编译和基本测试
3. 提交 PR 时请详细描述修改内容

## 许可证

本项目遵循 MIT License。

## 作者

- **孙旭升** - [Sunxs1020@gmail.com](mailto:Sunxs1020@gmail.com)

---

如有问题或建议，欢迎提交 issue 或 PR。
