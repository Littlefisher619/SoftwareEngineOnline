import homework from "../api/homework"

export const info = (state, user) => {
    state.user = JSON.parse(JSON.stringify(user))
}
export const homeworkName = (state, homeworkName) => {
    state.homework.homeworkname = JSON.parse(JSON.stringify(homeworkName))
}