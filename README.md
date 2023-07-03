# Modeling...

普通にモデリングしても途中で飽きて完成しないので、
プログラムに寄せて、システマティックにやってみようという企画。

## 設計

- HumanoidRig を組む
- Bone の方向が定まる
- 決まった Bone の方向に合わせた部品を `サイズ1` で作る
  - WeightPaint せずに Object の parent を Armature の Bone に指定する手法を使う
  - 関節は曲がらないので、ロボットや人形のようなデザインにする
- 組み立てるときに、 部品を `Bone の長さ` でスケールする
- 左右対称の部品は左側を作成して `-x` スケールにする

## making

- [day1](docs/day001.md)
- [day2](docs/day002.md)
- [day3](docs/day003.md)
